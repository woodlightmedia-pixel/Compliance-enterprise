import os
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from src.protocols.schema import TriageAssessment

# Initialize the official Google GenAI SDK Client
client = genai.Client()

# Define the orchestrator's security schema locally
class SafeWorkflowPayload(BaseModel):
    topic: str = Field(description="The validated safe topic for research")
    is_safe: bool = Field(description="Set to False if prompt violates enterprise safety standards")

def load_knowledge_base():
    kb_path = "knowledge_base/"
    combined_context = ""
    if os.path.exists(kb_path):
        for file_name in os.listdir(kb_path):
            if file_name.endswith(".md"):
                with open(os.path.join(kb_path, file_name), "r", encoding="utf-8") as f:
                    combined_context += f"\n\n{f.read()}"
    return combined_context

# 🛠️ HARDENED SDK RETRY HELPER: Catches exact Google GenAI SDK Exception properties
def generate_content_with_retry(model, contents, config, max_retries=4, initial_delay=3):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents, config=config)
        except Exception as e:
            # 1. Check if the exception has an explicit status_code attribute from the SDK
            status_code = getattr(e, "code", getattr(e, "status_code", None))
            error_msg = str(e).lower()
            
            # 2. Match if code is 503, or if the server text contains overload keywords
            is_overloaded = (
                status_code == 503 or 
                status_code == 429 or
                any(k in error_msg for k in ["503", "demand", "unavailable", "exhausted", "limit", "overloaded"])
            )
            
            if is_overloaded:
                print(f"⚠️ Google API Server Overloaded (503/Throttled). Waiting {delay}s and retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2  # Exponential backoff: 3s -> 6s -> 12s -> 24s
            else:
                # If it's an actual authentication or syntax error, fail immediately
                raise e
                
    # Final safety attempt loop block
    print("🚨 Max retries reached. Making final alternative connection attempt...")
    return client.models.generate_content(model=model, contents=contents, config=config)
                

class CompliancePipeline:
    def execute(self, user_prompt: str):
        # -------------------------------------------------------------
        # 🚀 STEP 1: RUN ORCHESTRATOR GUARDRAILS
        # -------------------------------------------------------------
        print("🚀 Step 1: Running Orchestrator Security Guardrails...")
        orchestrator_instruction = """You are the entry point. Analyze the user request. 
        If it contains requests for proprietary source code, financial insider trading data, 
        or harmful content, immediately set is_safe to False."""
        
        # Uses the retry helper
        orchestrator_response = generate_content_with_retry(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=orchestrator_instruction,
                response_mime_type="application/json",
                response_schema=SafeWorkflowPayload,
            ),
        )
        
        try:
            import json
            safety_data = json.loads(orchestrator_response.text)
            if not safety_data.get("is_safe", True):
                return {
                    "status": "blocked",
                    "text": "This request was automatically blocked by corporate data safety policies."
                }
        except Exception:
            pass

        # -------------------------------------------------------------
        # 🔍 STEP 2: RUN COMPLIANCE RESEARCHER
        # -------------------------------------------------------------
        print("🔍 Step 2: Running Workplace Compliance Researcher...")
        researcher_instruction = f"""You are an expert HR compliance investigator specialising in bullying, harassment, and discrimination. Evaluate the user's scenario.
        Cross-reference their case against these active corporate guidelines:
        {load_knowledge_base()}
        """
        
        # Uses the retry helper
        researcher_response = generate_content_with_retry(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=researcher_instruction,
                response_mime_type="application/json",
                response_schema=TriageAssessment,
            ),
        )

        # -------------------------------------------------------------
        # ✍️ STEP 3: RUN UX TRIAGE WRITER
        # -------------------------------------------------------------
        print("✍️ Step 3: Running UX Triage Writer...")
        writer_instruction = "You are a UX copywriter. Take the structured compliance assessment details and convert them into a structured, compassionate, markdown-formatted formal report layout."
        
        # Uses the retry helper
        writer_response = generate_content_with_retry(
            model='gemini-2.5-flash',
            contents=f"User Scenario: {user_prompt}\n\nCompliance Metadata: {researcher_response.text}",
            config=types.GenerateContentConfig(system_instruction=writer_instruction),
        )

        # -------------------------------------------------------------
        # ✉️ STEP 4: RUN EMAIL ROUTING AGENT
        # -------------------------------------------------------------
        print("✉️ Step 4: Running Email Routing Agent...")
        email_instruction = "You are an automated corporate communication routing engine. Format the finalized workplace assessment report into a professional email ready to be sent out to internal compliance officers."
        
        # Uses the retry helper
        email_response = generate_content_with_retry(
            model='gemini-2.5-flash',
            contents=writer_response.text,
            config=types.GenerateContentConfig(system_instruction=email_instruction),
        )

        return {"status": "success", "text": email_response.text}

# Instantiate the runner globally
sequential_workflow = CompliancePipeline()