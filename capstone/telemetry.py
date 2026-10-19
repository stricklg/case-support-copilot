import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

LOG_FILE_PATH = Path(__file__).resolve().parent / "telemetry_events.jsonl"

class TelemetryEvent(BaseModel):
    """Structured telemetry event created at every pipeline boundry."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ticket_id: str
    stage: str # "INGESTION", "RETRIEVAL", "TRIAGE", "EXECUTION"
    status: str # "SUCCESS", "REJECTED", "DEFLECTED", "ERROR"
    latency_ms: float
    details: Dict[str, Any] = Field(default_factory=dict)

def log_event(event: TelemetryEvent, log_path: Path = LOG_FILE_PATH) -> None:
    """Appends a structured JSON event to the audit log."""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(event.model_dump_json() + "\n")