## Architecture Diagram
```mermaid
flowchart TD
    %% Node Definitions & Shapes
    USER([User / Ticket Ingestion])
    
    subgraph Ingestion ["1. Defensive Ingestion & Sanitization"]
        P_IN{Pydantic Inbound Contract}
        CLEAN[Data Cleaning & OCR / Normalization]
        IN_REJECT[Reject & Alert Source: 400 Bad Request]
    end

    subgraph Retrieval ["2. Grounded Retrieval (RAG)"]
        KB[(Vector DB: Policy & Runbooks)]
        V_GATE{Similarity Score >= Threshold?}
        DEFLECT[Deflection Guardrail: No KB Match]
    end

    subgraph Inference ["3. Tiered Inference & Schema Validation"]
        LLM1[Primary Tier: Gemini 1.5 Flash + Enforced Schema]
        GATE1{LLM 1 Valid JSON & Score >= 5?}
        LLM2[Fallback Tier: Gemini 1.5 Pro + Enforced Schema]
        GATE2{LLM 2 Valid JSON & Score >= 5?}
    end

    subgraph Egress ["4. Egress Validation & Resolution"]
        P_OUT[Pydantic Outbound Contract: Strict JSON]
        AUTO_ACTION[Autonomous Tool Dispatch / API Resolution]
        HITL[Human-in-the-Loop Review Queue]
        USER_SLA[User Message: Support Rep will reach out in 3 days]
    end

    subgraph Observability ["5. Audit Telemetry & Offline Evals"]
        AUDIT[(Append-Only JSONL Audit Stream)]
        EVAL[Offline LLM-as-a-Judge Eval Harness]
    end

    %% Workflow Connections
    USER --> P_IN
    P_IN -->|Schema Valid| CLEAN
    P_IN -->|Malformed Payload| IN_REJECT
    
    CLEAN --> KB
    KB --> V_GATE
    V_GATE -->|Grounded Context Found| LLM1
    V_GATE -->|No Relevant Context| DEFLECT
    
    LLM1 --> GATE1
    GATE1 -->|Success & High Confidence| P_OUT
    GATE1 -->|Rate Limit / Timeout / Score < 5| LLM2
    
    LLM2 --> GATE2
    GATE2 -->|Success & High Confidence| P_OUT
    GATE2 -->|Parse Error / Score < 5| HITL
    
    P_OUT --> AUTO_ACTION
    DEFLECT --> HITL
    HITL --> USER_SLA
    
    %% Telemetry Logging Streams (Dotted lines)
    P_IN -.-> AUDIT
    V_GATE -.-> AUDIT
    GATE1 -.-> AUDIT
    GATE2 -.-> AUDIT
    P_OUT -.-> AUDIT
    HITL -.-> AUDIT
    AUDIT --> EVAL

    %% Styling
    classDef boundary fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef fallback fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef data fill:#ede7f6,stroke:#4527a0,stroke-width:2px;
    classDef success fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

    class P_IN,V_GATE,GATE1,GATE2 boundary;
    class IN_REJECT,DEFLECT,LLM2,HITL,USER_SLA fallback;
    class KB,AUDIT,EVAL data;
    class AUTO_ACTION,P_OUT success;
```