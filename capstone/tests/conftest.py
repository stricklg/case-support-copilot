"""Pytest setup: make the capstone package importable and
keep every test offline.

main.py builds a genai.Client at import time, so a dummy key
must exist in the environment before any test module imports
it. No test makes a network call - the suites cover the
deterministic seams (dispatch gates, validation, pricing,
the regression gate), not the live models.
"""
import os
import sys
from pathlib import Path

CAPSTONE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CAPSTONE_DIR))
sys.path.insert(0, str(CAPSTONE_DIR / "eval"))
os.chdir(CAPSTONE_DIR)

os.environ.setdefault("GEMINI_API_KEY", "test-dummy-key")
os.environ.setdefault("OPENAI_API_KEY", "test-dummy-key")
