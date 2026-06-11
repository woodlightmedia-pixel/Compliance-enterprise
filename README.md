# Compliance & Enterprise Tool Engine

An asynchronous multi-agent compliance pipeline built with FastAPI and the modern `google-genai` SDK, featuring vector-based RAG retrieval and native tool-calling capabilities.

## 📁 Repository Structure

```text
├── src/
│   ├── enterprise/
│   │   ├── guardrails.py        # Input verification and policy checks
│   │   ├── mcp_client.py        # Asynchronous multi-agent pipeline controller
│   │   ├── mcp_orchestrator.py  # Gemini client configuration & native tool routing
│   │   └── rag_engine.py        # Vector database lookup connector
│   │
│   ├── protocols/
│   │   ├── router.py            # API ingress route endpoints
│   │   └── schema.py            # Pydantic validation payload classes
│   │
│   └── main.py                  # ASGI application entrypoint
│
├── requirements.txt             # Project dependencies manifest
└── README.md                    # System documentation