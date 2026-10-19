import time
from pathlib import Path
from dotenv import load_dotenv
from context_engine import KB
from main import run_pipeline
from schemas import InboundTicket
import streamlit as st

load_dotenv(Path(__file__).resolve().parent / ".env")

st.set_page_config(
    page_title="AI Support Triage & RAG", page_icon="🤖", layout="wide"
)

@st.cache_resource
def load_kb():
    kb_dir = Path(__file__).resolve().parent / "kb"
    kb = KB(kb_dir=kb_dir)
    kb.build_index()
    return kb

with st.spinner("Initializing KB index..."):
    kb = load_kb()

st.title("🤖Customer Support Triage Assistant")
st.markdown("Automated RAG triage, similarity gating, and policy routing.")

#Layout: Input form on left, Output & Telemetry on right
col1, col2 = st.columns([1,1], gap="medium")

with col1:
    st.subheader("Submit Support Ticket")

    with st.form("ticket_form"):
        ticket_id = st.text_input("Ticket ID", value=f"TICK-{int(time.time())}")
        customer_email = st.text_input(
            "Customer Email", placeholder="customer@email.com"
        )
        subject = st.text_input(
            "Subject", placeholder="e.g., Webhook 500 errors on delivery"
        )
        body = st.text_area(
            "Message Body",
            height=180,
            placeholder=(
                "Describe the issue (e.g., Our endpoint keeps receiving 504 gateway"
                " timeouts when processing your webhook notifications...)"
            ),
        )

        submitted = st.form_submit_button("Submit & Triage", type="primary")

with col2:
    st.subheader("Triage Decision & Trace")

    if submitted:
        if not subject.strip() or not body.strip() or not customer_email.strip():
            st.error("Please provide both an email, subject and message body.")
        else:
            try:
                ticket = InboundTicket(
                    ticket_id=ticket_id.strip(),
                    customer_email=customer_email.strip(), 
                    subject=subject.strip(),
                    body=body.strip(),
                )

                with st.spinner("Running retrieval and triage..."):
                    start_t = time.perf_counter()

                    status_code, result = run_pipeline(ticket.model_dump(), kb)
                    total_ms = (time.perf_counter() - start_t) * 1000
                    execution = result.get("execution", {}) if isinstance(result, dict) else {}
                    destination = (
                        execution.get("destination")
                        if isinstance(execution, dict)
                        else getattr(execution, "destination", "UNKNOWN")
                    )

                    if destination == "AUTOMATED_CRM":
                        st.success(f"Routed to **AUTOMATED_QUEUE_CRM** ({total_ms:.0f} ms)")
                    elif destination == "HITL_QUEUE":
                        st.warning(f"Routed to **HITL_QUEUE** ({total_ms:.0f} ms)")
                    else:
                        st.info(f"Routed to: **{destination}** ({total_ms:.0f} ms)")

                    st.markdown("### Output Details")
                    st.json(result if isinstance(result, dict) else result.model_dump())

            except Exception as e:
                st.error(f"Pipeline error: {e}")

    else:
        st.info("Submit a ticket on the left to inspect real-time routing.")
            
