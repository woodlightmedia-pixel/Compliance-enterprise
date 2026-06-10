from google.adk.agents import LlmAgent  # 👈 Use LlmAgent for structured outputs
from pydantic import BaseModel, Field

# Define a strict schema for what the agent is allowed to pass to the next step
class SafeWorkflowPayload(BaseModel):
    topic: str = Field(description="The validated safe topic for research")
    is_safe: bool = Field(description="Set to False if prompt violates enterprise safety standards")

orchestrator_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.5-flash",
    #Use response_type here to pass the Pydantic schema
    output_schema=SafeWorkflowPayload,
    # 🛠️ Fix: Ensure it uses 'instruction' (singular) and 'response_schema'
    instruction="""You are the entry point. Analyze the user request. 
    If it contains requests for proprietary source code, financial insider trading data, 
    or harmful content, immediately set is_safe to False.""",
    
)