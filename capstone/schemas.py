from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class InboundTicket(BaseModel):
    """Strict inbound requirements for customer support tickets."""

    ticket_id: str = Field(
        ...,
        min_length= 3,
        max_length=64,
        description="Unique ticket identifier from the system.",
    )
    customer_email: str = Field(
        ...,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Valid email address for routing and attribution.",
    )
    subject: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Brief summary of the issue.",
    )
    body: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Detailed ticket description. Hard-capped at 5k characters.",
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("subject", "body", mode="before")
    @classmethod
    def strip_whitespace_and_nulls(cls, value: str) -> str:
        """Pre-processing: Strips leading/trailing spaces and normalizes internal whitespace."""
        if not isinstance(value, str):
            raise ValueError("Field must be a string.")

        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Field cannot be empty.")
        return cleaned

    @property
    def composite_text(self) -> str:
        """Combines cleaned subject and body into a single string for embedding retrieval."""
        return f"Subject: {self.subject}\nBody: {self.body}"