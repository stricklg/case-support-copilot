import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from google import genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

@dataclass
class RetrievalResult:
    is_deflected: bool
    similarity_score: float
    matched_kb: Optional[str] = None
    matched_content: Optional[str] = None

class KB:
    def __init__(
            self,
            kb_dir: Path,
            similarity_threshold: float = 0.65,
            model: str = "gemini-embedding-001",
    ):
        self.client = genai.Client()
        self.kb_dir = kb_dir
        self.threshold = similarity_threshold
        self.embedding_model = model

        # In-memory storage: {filename: (normalized_vector, raw_markdown_text)}
        self.index: Dict[str, Tuple[np.ndarray, str]] = {}

    def _embed_text(self, text: str) -> np.ndarray:
        """Generates and normalizes an embedding vector for unit-length dot product math."""
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
        """Scans KB directory, embeds all md files and builds the in-memory store."""
        files = list(self.kb_dir.rglob("*.md"))
        if not files:
            raise FileNotFoundError(
                f"No md KB found in {self.kb_dir}"
            )
        print(f"Indexing {len(files)} KB's...")
        for file_path in files:
            content = file_path.read_text(encoding="utf-8")
            norm_vec = self._embed_text(content)
            self.index[file_path.name] = (norm_vec, content)
            print(f"Indexed: {file_path.name}")
        print("Vector store indexing complete.\n")

    def query(self, ticket_text: str) -> RetrievalResult:
        """Computes cosine similarity across all KB and evaluates the threshold gate."""
        if not self.index:
            raise RuntimeError("Vectore store index is empty. Call build_index() first.")

        query_vec = self._embed_text(ticket_text)

        best_score = -1.0
        best_file = None
        best_content = None

        for filename, (doc_vec, doc_content) in self.index.items():
            score = float(np.dot(query_vec, doc_vec))
            if score > best_score:
                best_score = score
                best_file = filename
                best_content = doc_content

        if best_score < self.threshold:
            return RetrievalResult(
                is_deflected=True,
                similarity_score=best_score,
                matched_kb=None,
                matched_content=None,
            )
        return RetrievalResult(
            is_deflected=False,
            similarity_score=best_score,
            matched_kb=best_file,
            matched_content=best_content,
        )