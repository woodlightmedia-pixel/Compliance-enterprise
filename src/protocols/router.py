import os
from fastapi import APIRouter, HTTPException
from src.protocols.schema import CaseSubmissionPayload
# 🚀 Clean imports - no Session class needed!
from src.workflow.sequence import sequential_workflow

router = APIRouter(prefix="/api/v1/message", tags=["Compliance"])

@router.post("/send")
async def process_compliance_case(payload: CaseSubmissionPayload):
    try:
        # 1. Extract the raw text input from the incoming Streamlit payload
        user_input_text = payload.message["parts"][0]["text"]
        
        # 2. Run the custom sequential workflow pipeline
        workflow_results = sequential_workflow.execute(user_input_text)
        
        # 3. 🛠️ FIXED: Safely unpack the string out of our custom pipeline dictionary
        if isinstance(workflow_results, dict):
            if workflow_results.get("status") == "blocked":
                final_output = workflow_results.get("text", "Blocked by safety guidelines.")
            else:
                # Look for 'text' first (what our custom pipeline uses), fallback to 'output' or 'analysis'
                final_output = workflow_results.get("text", workflow_results.get("output", workflow_results.get("analysis", str(workflow_results))))
        elif hasattr(workflow_results, "text"):
            final_output = workflow_results.text
        else:
            final_output = str(workflow_results)

        # 4. Ship a clean, flat dictionary back to the Streamlit frontend
        return {
            "status": "blocked" if isinstance(workflow_results, dict) and workflow_results.get("status") == "blocked" else "success",
            "analysis": final_output
        }

    except Exception as e:
        print(f"\n❌ CRITICAL CRASH IN ROUTER ENDPOINT: {str(e)}\n")
        raise HTTPException(
            status_code=500, 
            detail=f"Pipeline internal processing error: {str(e)}"
        )