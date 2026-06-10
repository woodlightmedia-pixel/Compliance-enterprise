# .truefoundry/deploy_prod.py
import os
from truefoundry.deploy import Service, Build, DockerfileBuild, Secret

service = Service(
    name="workplace-dignity-platform-prod",
    image=Build(build_source=DockerfileBuild(dockerfile_path="../Dockerfile")),
    
    # 🔒 Production Domain routing over secure TLS/HTTPS
    ports=[{"port": 8000, "host": "compliance.yourcompany.com"}],
    
    # 🛡️ Inject live production keys safely from the cloud secret store
    env={
        "APP_ENV": "production",
        "GEMINI_API_KEY": Secret.from_kv_secret("prod-llm-credentials", "GEMINI_API_KEY"),
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_SENDER_EMAIL": "secure-compliance@yourcompany.com",
        "SMTP_SENDER_PASSWORD": Secret.from_kv_secret("prod-email-credentials", "SMTP_PASSWORD")
    },
    
    # Enable hardened platform-level guardrails & A2A governance profiles
    labels={
        "tfy.agentic.governance": "enabled",
        "tfy.agent.protocol": "a2a",
        "tfy.environment": "production"
    },
    configuration={
        "gateway_policies": {
            "prompt_injection_protection": True,
            "pii_masking": {"enabled": True, "action": "redact"},
            "rate_limiting": {"requests_per_minute": 30} # Prevent brute-force token draining
        }
    }
)

# Deploy straight to your live corporate AWS EKS cluster
service.deploy(workspace_fqn="aws-prod-cluster:main-compliance-space")