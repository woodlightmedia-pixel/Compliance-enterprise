# src/enterprise/mcp_client.py
import os

# 🔍 UNIVERSAL DIAGNOSTIC PRINT (Zero f-strings, Zero backslashes)
debug_key = os.environ.get("GEMINI_API_KEY", "")
print("🔥 DEPLOYMENT DEBUG INFO 🔥")
print("Key Found in Env:", bool(debug_key))
print("Key Exact Character Length:", len(debug_key))
print("Key Starts With:", debug_key[:6])

import logging
from contextlib import AsyncExitStack
from google import genai
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Import your RAG function to fetch context from Pinecone v2
from src.enterprise.rag_engine import retrieve_compliance_context

logger = logging.getLogger("compliance-backend.mcp_client")

class ModelContextProtocolClient:
    """Handles the low-level connection handshake with internal tool scripts."""
    def __init__(self):
        self.session = None
        self._exit_stack = AsyncExitStack()

    async def connect_to_tools(self, server_path: str = "src/enterprise/mcp_server.py"):
        if not os.path.exists(server_path):
            return False
        server_params = StdioServerParameters(command="python3", args=[server_path])
        try:
            read, write = await self._exit_stack.enter_async_context(stdio_client(server_params))
            self.session = await self._exit_stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            return True
        except Exception as e:
            logger.error(f"MCP Init Error: {str(e)}")
            return False


# 🔥 THE FIX: Add **kwargs to safely absorb extra parameters like 'context_documents'
async def execute_mcp_agent_pipeline(user_scenario: str, **kwargs) -> str:
    """
    Executes the full end-to-end compliance workflow:
    1. Queries Pinecone RAG for legal references.
    2. Bridges over to the tool-calling enterprise orchestrator pipeline.
    """
    try:
        logger.info("🎬 Initializing Compliance Multi-Agent Pipeline...")
        
        # (Optional) If you ever want to access those passed documents later:
        passed_docs = kwargs.get("context_documents", [])

        # Step 1: Pull semantic data out of your newly populated Pinecone index
        logger.info("🧠 Fetching policy framework from Pinecone RAG...")
        compliance_context = retrieve_compliance_context(user_scenario)

        # ⚡ BRIDGE THE GAP: Hand execution off to your tool-calling orchestrator!
        from .mcp_orchestrator import execute_enterprise_pipeline
        
        analysis_result = await execute_enterprise_pipeline(
            user_prompt=user_scenario,
            compliance_context=compliance_context
        )

        return analysis_result

    except Exception as e:
        logger.error(f"❌ Critical failure in agent execution pipeline: {str(e)}")
        return f"Pipeline Error processing request: {str(e)}"

