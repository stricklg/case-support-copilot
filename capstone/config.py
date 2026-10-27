import os
from dotenv import load_dotenv

load_dotenv()

PRIMARY_MODEL = os.getenv('PRIMARY_MODEL', 'gemini-3.5-flash-lite')
FALLBACK_MODEL = os.getenv('FALLBACK_MODEL', 'gemini-3.8-flash')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'gemini-embedding-001')

SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.65'))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.65'))

JUDGE_MODEL = os.getenv('JUDGE_MODEL', 'gpt-6.1-sol')
# Keyword-rescue gate (hybrid retrieval): when the vector winner is
# below SIMILARITY_THRESHOLD, a match is still accepted if BM25
# independently ranks a chunk from the same document first, by at
# least this margin over the runner-up, and the cosine is at least
# the floor below. Calibrated on the 50-case golden set (2026-10-27).
KEYWORD_RESCUE_MIN_SIMILARITY = float(
    os.getenv('KEYWORD_RESCUE_MIN_SIMILARITY', '0.60'))
KEYWORD_RESCUE_MARGIN = float(
    os.getenv('KEYWORD_RESCUE_MARGIN', '1.25'))
