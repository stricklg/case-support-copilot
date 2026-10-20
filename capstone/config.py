import os
from dotenv import load_dotenv

load_dotenv()

PRIMARY_MODEL = os.getenv('PRIMARY_MODEL', 'gemini-3.5-flash-lite')
FALLBACK_MODEL = os.getenv('FALLBACK_MODEL', 'gemini-3.8-flash')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'gemini-embedding-001')

SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.65'))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.65'))

JUDGE_MODEL = os.getenv('JUDGE_MODEL', 'gpt-6.1-sol')