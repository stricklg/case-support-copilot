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

# Margin floor (dispatch): when the winning runbook only narrowly
# beats the best chunk from any other runbook, the match is
# contested and the ticket goes to human review regardless of the
# model's self-reported confidence. Calibrated on the 50-case
# golden set (2026-10-27): all three category errors measured
# that day (G10, G44, G45) had margins at or below 0.057 while
# carrying self-reported confidence 0.95, and the top half of
# margins (>= 0.083) had zero errors. In-sample calibration;
# revisit as the golden set grows.
MARGIN_FLOOR = float(os.getenv('MARGIN_FLOOR', '0.05'))
