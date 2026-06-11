# src/protocols/router.py
import os
import logging
from fastapi import APIRouter, HTTPException
from src.protocols.schema import CaseSubmissionPayload

# 🚀 NEW ENTERPRISE IMPORTS (Fully Connected)
from src.enterprise.guardrails import run_ingress_guardrail
from src.enterprise.mcp_client import execute_mcp_agent_pipeline

# Configure contextual logging output
logger = logging.getLogger("compliance-backend.router")

router = APIRouter(prefix="/api/v1/message", tags=["Compliance"])

@router.post("/send")
async def send_compliance_case(payload: CaseSubmissionPayload):
    try:
        # Extract and map incoming payload strings cleanly
        user_input_text = payload.message
        logger.info("📩 Received compliance processing request payload.")

        # ---------------------------------------------------------
        # 🛡️ STEP 1: RUN INGRESS GUARDRAIL (Centralized Security)
        # ---------------------------------------------------------
        logger.info("🛡️ Running security ingress guardrails...")
        security_check = run_ingress_guardrail(user_input_text)
        
        # If the guardrail object triggers an alert, halt execution early
        if not getattr(security_check, "is_safe", True):
            risk = getattr(security_check, "risk_category", "Corporate Policy Violation")
            logger.warning(f"⚠️ Request BLOCKED by Ingress Guardrail. Category: {risk}")
            return {
                "status": "blocked",
                "analysis": f"Security Guardrail Active: Request blocked under category [{risk}]."
            }

        # ---------------------------------------------------------
        # 🤖 STEP 2: EXECUTE COGNITIVE PIPELINE WITH MCP TOOLS (Awaited!)
        # ---------------------------------------------------------
        # Note: Semantic RAG retrieval from Pinecone is handled automatically 
        # inside your execute_mcp_agent_pipeline code!
        logger.info("🚀 Launching multi-agent orchestrator loop...")
        workflow_results = await execute_mcp_agent_pipeline(user_scenario=user_input_text)
        
        # ---------------------------------------------------------
        # 📦 STEP 3: ROBUST UNPACKING (Keeps system outputs flat and predictable)
        # ---------------------------------------------------------
        logger.info("📦 Sanitizing agent report structures for UI delivery...")
        if isinstance(workflow_results, dict):
            if workflow_results.get("status") == "blocked":
                final_output = workflow_results.get("text", "Blocked by safety guidelines.")
            else:
                # Target common payload keys sequentially
                final_output = workflow_results.get(
                    "text", 
                    workflow_results.get(
                        "output", 
                        workflow_results.get("analysis", str(workflow_results))
                    )
                )
        elif hasattr(workflow_results, "text"):
            final_output = workflow_results.text
        else:
            final_output = str(workflow_results)

        # Step 4: Return pristine telemetry data directly to the Streamlit layout
        return {
            "status": "blocked" if isinstance(workflow_results, dict) and workflow_results.get("status") == "blocked" else "success",
            "analysis": final_output
        }

    except Exception as e:
        logger.critical(f"❌ CRITICAL CRASH IN ROUTER ENDPOINT: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Enterprise Pipeline processing error: {str(e)}"
        )