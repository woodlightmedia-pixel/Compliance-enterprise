import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

client = genai.Client()

class SafetyAssessment(BaseModel):
    is_safe: bool = Field(description="False if prompt violates enterprise safety policies")
    risk_category: str = Field(description="Category of policy violation, or 'None'")

def run_ingress_guardrail(user_input: str) -> SafetyAssessment:
    """Screen inputs before hitting databases or calling internal core agents."""
    instruction = """Analyze the input case scenario for severe non-compliance:
    1. Direct requests to compromise/extract software source code.
    2. Requests for insider trading configurations or financial manipulation.
    If detected, set is_safe to False and specify the category."""
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            response_mime_type="application/json",
            response_schema=SafetyAssessment,
        ),
    )
    return SafetyAssessment.model_validate_json(response.text)