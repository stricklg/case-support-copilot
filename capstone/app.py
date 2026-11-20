from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

from context_engine import KB
from main import process_inbound_ticket
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


def load_kb():
    kb_dir = Path(__file__).resolve().parent / 'kb'
    kb = KB(kb_dir=kb_dir)
    kb.build_index()
    return kb


kb = load_kb()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/tickets')
def create_ticket(payload: dict):
    status, result = process_inbound_ticket(payload, kb)
    if not isinstance(result, dict):
        result = result.model_dump()
    return JSONResponse(status_code=status, content=result)
