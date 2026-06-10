# 1. Import individual agents from their respective files
from .orchestrator import orchestrator_agent
from .researcher import researcher_agent
from .writer import writer_agent        # Make sure this matches your writer filename
from .email import email_agent          # Make sure this matches your email filename

# 2. Expose them globally to the rest of your system
__all__ = [
    "orchestrator_agent",
    "researcher_agent",
    "writer_agent",
    "email_agent"
]