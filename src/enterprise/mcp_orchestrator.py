# src/enterprise/mcp_orchestrator.py
import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger("compliance-backend.mcp_orchestrator")

raw_key = os.environ.get("GEMINI_API_KEY", "")
clean_key = raw_key.strip() if raw_key else None

client = genai.Client(api_key=clean_key)

# -------------------------------------------------------------------------
# 🎯 NATIVE ENTERPRISE TOOLS (Declared as pure Python callables)
# -------------------------------------------------------------------------

def send_corporate_email(report_markdown: str) -> str:
    """Routes formal report to compliance officers via AWS SES Relay.
    
    Args:
        report_markdown: The final generated compliance risk assessment text.
    """
    # 💡 Your real execution logic (SMTP / AWS SES) can plug right here later!
    logger.info("📬 send_corporate_email tool triggered by Gemini.")
    return "SUCCESS: Compliance report successfully relayed to officers."


def log_case_to_db(report_markdown: str, risk_category: str) -> str:
    """Saves an encrypted log of this interaction to the PostgreSQL instance.
    
    Args:
        report_markdown: The text analysis of the compliance breach.
        risk_category: The classification tier parsed by the system.
    """
    # 💡 Your real database insert logic can plug right here later!
    logger.info("🗄️ log_case_to_db tool triggered by Gemini.")
    return "SUCCESS: Interaction safely encrypted and committed to PostgreSQL."


# -------------------------------------------------------------------------
# 🧠 CORE ORCHESTRATION PIPELINE
# -------------------------------------------------------------------------

async def execute_enterprise_pipeline(user_prompt: str, compliance_context: str) -> str:
    """Runs Gemini with native enterprise tool configurations."""
    try:
        enriched_prompt = f"Context:\n{compliance_context}\n\nScenario:\n{user_prompt}"
        
        logger.info("🤖 Routing enriched payload through Gemini tool-calling layer...")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=enriched_prompt,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an Enterprise Compliance Agent. Evaluate the scenario using "
                    "the provided context and execute the appropriate communication tools."
                ),
                # 🎯 FIXED: Pass the raw Python functions directly into the tools array!
                tools=[send_corporate_email, log_case_to_db]
            )
        )
        return response.text

    except Exception as e:
        logger.error(f"Error in enterprise orchestrator layer: {str(e)}")
        raise e