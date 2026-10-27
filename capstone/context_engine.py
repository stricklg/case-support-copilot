import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from google import genai
from dotenv import load_dotenv
from config import (
    SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL,
    KEYWORD_RESCUE_MIN_SIMILARITY,
    KEYWORD_RESCUE_MARGIN,
)
import numpy as np

load_dotenv()


@dataclass
class RetrievalResult:
    is_deflected: bool
    similarity_score: float
    margin: float = 0.0
    matched_kb: Optional[str] = None
    matched_content: Optional[str] = None


def _tokens(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _split_chunks(content: str) -> List[str]:
    """Split a runbook into section chunks.

    Each chunk is the document header (title, category, applies-to)
    prepended to one '## ' section, so a chunk keeps its topic
    anchor while scoring on its own content instead of diluting
    into a whole-document average. Sections whose heading contains
    'escalation' are excluded: that text is routing policy, not
    answer content, and its generic urgency vocabulary otherwise
    out-competes the substantive section for problem-worded
    tickets (measured 2026-10-27: it won 17 of 33 judged cases
    and those replies scored 1-2).
    """
    parts = re.split(r"(?m)^(## .*)$", content)
    header = parts[0].strip()
    chunks = []
    for i in range(1, len(parts), 2):
        if "escalation" in parts[i].lower():
            continue
        section = (parts[i] + parts[i + 1]).strip()
        chunks.append(header + "\n\n" + section)
    if not chunks:
        chunks.append(content.strip())
    return chunks


class KB:
    """Chunked hybrid retrieval over the runbook collection.

    Ranking is by embedding cosine over section chunks. The gate
    accepts a match when the best cosine clears the similarity
    threshold, or when the keyword-rescue fires: BM25 independently
    ranks a chunk from the same document first, by the configured
    margin, with the cosine above the rescue floor. BM25 never
    picks the winner - it only corroborates the vector winner -
    so keyword noise cannot change which document answers.
    """

    def __init__(
            self,
            kb_dir: Path,
            similarity_threshold: float = SIMILARITY_THRESHOLD,
            model: str = EMBEDDING_MODEL,
    ):
        self.client = genai.Client()
        self.kb_dir = kb_dir
        self.threshold = similarity_threshold
        self.embedding_model = model

        # Chunks: list of (doc_name, chunk_text, normalized_vector).
        # Chunks are the ranking unit; the context returned for a
        # match is the winning chunk's full parent document
        # (small-to-big retrieval), so reply drafting and judging
        # keep the complete runbook.
        self.chunks: List[Tuple[str, str, np.ndarray]] = []
        # Kept for compatibility: {filename: (doc_vector, raw_text)}
        self.index: Dict[str, Tuple[np.ndarray, str]] = {}
        self._chunk_tokens: List[List[str]] = []
        self._df: Counter = Counter()
        self._avgdl: float = 0.0

    def _embed_text(self, text: str) -> np.ndarray:
        """Generates and normalizes an embedding vector for
        unit-length dot product math."""
        response = self.client.models.embed_content(
            model=self.embedding_model,
            contents=text,
        )

        if hasattr(response, "embedding") and response.embedding:
            raw_values = response.embedding.values
        else:
            raw_values = response.embeddings[0].values

        vec = np.array(raw_values, dtype=np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def build_index(self):
        """Scans KB directory, chunks and embeds all md files,
        and builds the in-memory vector + BM25 stores."""
        files = list(self.kb_dir.rglob("*.md"))
        if not files:
            raise FileNotFoundError(
                f"No md KB found in {self.kb_dir}"
            )
        print(f"Indexing {len(files)} KB's...")
        for file_path in files:
            content = file_path.read_text(encoding="utf-8")
            self.index[file_path.name] = (
                self._embed_text(content), content)
            for chunk_text in _split_chunks(content):
                vec = self._embed_text(chunk_text)
                self.chunks.append(
                    (file_path.name, chunk_text, vec))
                toks = _tokens(chunk_text)
                self._chunk_tokens.append(toks)
                for w in set(toks):
                    self._df[w] += 1
            print(f"Indexed: {file_path.name} "
                  f"({len(_split_chunks(content))} chunks)")
        if self._chunk_tokens:
            self._avgdl = (sum(len(t) for t in self._chunk_tokens)
                           / len(self._chunk_tokens))
        print("Vector store indexing complete.\n")

    def _bm25_scores(self, query_text: str) -> List[float]:
        """Okapi BM25 over chunks, stdlib implementation."""
        n = len(self.chunks)
        query_terms = set(_tokens(query_text))
        scores = []
        k1, b = 1.5, 0.75
        for toks in self._chunk_tokens:
            tf = Counter(toks)
            dl = len(toks)
            s = 0.0
            for w in query_terms:
                if w not in tf:
                    continue
                idf = math.log(
                    1 + (n - self._df[w] + 0.5) / (self._df[w] + 0.5))
                denom = tf[w] + k1 * (1 - b + b * dl / self._avgdl)
                s += idf * (tf[w] * (k1 + 1) / denom)
            scores.append(s)
        return scores

    def _keyword_rescue(self, query_text: str,
                        vec_doc: str, vec_score: float) -> bool:
        """True when BM25 corroborates the vector winner strongly
        enough to accept a below-threshold cosine."""
        if vec_score < KEYWORD_RESCUE_MIN_SIMILARITY:
            return False
        bm = self._bm25_scores(query_text)
        order = sorted(range(len(bm)), key=lambda i: -bm[i])
        top_doc = self.chunks[order[0]][0]
        if top_doc != vec_doc:
            return False
        top = bm[order[0]]
        second = bm[order[1]] if len(order) > 1 else 0.0
        if second <= 0:
            return top > 0
        return top / second >= KEYWORD_RESCUE_MARGIN

    def query(self, ticket_text: str) -> RetrievalResult:
        """Ranks chunks by cosine, applies the hybrid gate, and
        returns the winning chunk's document and text."""
        if not self.chunks:
            raise RuntimeError(
                "Vector store index is empty. "
                "Call build_index() first.")

        query_vec = self._embed_text(ticket_text)

        best_score = -1.0
        best_doc = None
        best_content = None
        doc_best = {}
        for doc_name, chunk_text, chunk_vec in self.chunks:
            score = float(np.dot(query_vec, chunk_vec))
            if score > doc_best.get(doc_name, -1.0):
                doc_best[doc_name] = score
            if score > best_score:
                best_score = score
                best_doc = doc_name
                # Small-to-big: rank on the chunk, answer with
                # the whole parent document.
                best_content = self.index[doc_name][1]
        # Margin: how decisively the winning document beat the
        # best chunk from any other document. A near-zero margin
        # means the ticket is contested between two runbooks.
        others = [s for d, s in doc_best.items() if d != best_doc]
        margin = best_score - max(others) if others else best_score

        if best_score >= self.threshold:
            return RetrievalResult(
                is_deflected=False,
                similarity_score=best_score,
            margin=margin,
                matched_kb=best_doc,
                matched_content=best_content,
            )
        if self._keyword_rescue(ticket_text, best_doc, best_score):
            return RetrievalResult(
                is_deflected=False,
                similarity_score=best_score,
            margin=margin,
                matched_kb=best_doc,
                matched_content=best_content,
            )
        return RetrievalResult(
            is_deflected=True,
            similarity_score=best_score,
            margin=margin,
            matched_kb=None,
            matched_content=None,
        )
