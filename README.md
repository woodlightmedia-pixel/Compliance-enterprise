# 💼 Workplace Dignity & Compliance Multi-Agent System

An enterprise-grade, sequential multi-agent orchestration platform driven by **Google ADK v2.0** and **FastAPI**. This system allows employees to securely submit workplace scenarios (including bullying, harassment, and racial discrimination) for automated legal triage against internal policy, national statutory guidelines (Acas), local council metrics, and international treaties.

---

## 📂 System Architecture Blueprint

```text
sequential-agent-platform/
├── .truefoundry/               # Cloud Infrastructure blueprints
│   ├── deploy.py               # Sandbox Environment script
│   ├── deploy_prod.py          # Production AWS EKS deployment script
│   └── tfy-secret-manifest.yaml# Encrypted Vault Secrets configuration
├── knowledge_base/             # Core Knowledge Reference Templates
│   ├── 01_local_workplace_policy.md
│   ├── 02_national_guidelines.md
│   ├── 03_council_standards.md
│   └── 04_international_law.md
├── src/
│   ├── main.py                 # Core FastAPI Application initialization
│   ├── agents/                 # Specialized AI Personas
│   │   ├── __init__.py         # Consolidated Package Exports
│   │   ├── researcher.py       # Triage & Google Search fallback engine
│   │   ├── writer.py           # UX UI Formatter & Status Marker
│   │   └── email_agent.py      # Transactional Secure SMTP Dispatcher
│   ├── workflow/               # Graph Execution Controls
│   │   ├── __init__.py         # Package Exports
│   │   └── sequence.py         # Linear Graph Configuration (START ➔ END)
│   ├── protocols/              # Network & Communication Contracts
│   │   ├── __init__.py         # Package Exports
│   │   ├── routes.py           # FastAPI Router (/api/v1 endpoints)
│   │   └── schema.py           # Pydantic Structural Contracts
│   └── ui/
│       └── app.py              # Front-End Streamlit Dashboard Web Application
├── Dockerfile                  # Production Multi-Stage Slim Container
├── requirements.txt            # Explicit Dependency tracking list
└── .env                        # Local Sandbox Keys (Environment Protected)