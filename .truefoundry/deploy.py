import os
from truefoundry.deploy import Service, Build, DockerfileBuild, Image

service = Service(
    name="sequential-agent-service",
    image=Build(
        build_source=DockerfileBuild(dockerfile_path="../Dockerfile")
    ),
    ports=[{"port": 8000, "host": "sequential-agent.your-domain.com"}],
    env={
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "ENV": "production"
    },
    # Integrates seamlessly with TrueFoundry's June 2026 Agent Gateway
    labels={
        "tfy.agentic.governance": "enabled",
        "tfy.agent.protocol": "a2a"
    }
)
  # Inside .truefoundry/deploy.py
service = Service(
    name="sequential-agent-service",
    # ...,
    labels={
        "tfy.agentic.governance": "enabled",
        "tfy.agent.protocol": "a2a"
    },
    # Define platform-level guardrails
    configuration={
        "gateway_policies": {
            "prompt_injection_protection": True,
            "pii_masking": {"enabled": True, "action": "redact"},
            "rate_limiting": {"requests_per_minute": 60}
        }
    }
)  

# Deploy to your mapped AWS Cluster
service.deploy(workspace_fqn="your-aws-cluster:your-workspace")