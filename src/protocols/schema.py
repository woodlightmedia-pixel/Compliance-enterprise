from pydantic import BaseModel, Field
from typing import List, Optional

# =====================================================================
# 1. FRONTEND DATA INPUT CONTRACT
# =====================================================================
class EmailDeliveryPreferences(BaseModel):
    send_to_requestor: bool = Field(
        default=False, 
        description="Whether the requestor wants a personal reference copy sent to them."
    )
    requestor_email: Optional[str] = Field(
        default=None, 
        description="The email address of the employee/requestor."
    )
    send_to_compliance: bool = Field(
        default=False, 
        description="Whether this case needs formal escalation to a compliance officer."
    )
    compliance_officer_email: Optional[str] = Field(
        default=None, 
        description="Direct email destination for the allocated compliance officer or triage queue."
    )

class CaseSubmissionPayload(BaseModel):
    message: dict = Field(
        description="The nested message structure from the UI, e.g., {'parts': [{'text': '...'}]}"
    )
    email_preferences: EmailDeliveryPreferences = Field(
        description="The delivery configurations and addresses mapped from the Streamlit toggles."
    )


# =====================================================================
# 2. INTERNAL AGENT TRIAGE CONTRACT
# =====================================================================
class TriageAssessment(BaseModel):
    is_discrimination_or_harassment: bool = Field(
        description="True if the user situation violates workplace policy, national guidelines, or international law."
    )
    severity_level: str = Field(
        description="Must be exactly one of: 'LOW', 'MEDIUM', or 'IMMEDIATE ACTION'."
    )
    applicable_frameworks: List[str] = Field(
        description="List of specific documents or statutes violated (e.g., 'Equality Act 2010', 'Local Policy Sec 2')."
    )
    recommended_escalation_path: str = Field(
        description="The primary internal or external body to contact (e.g., 'Internal HR', 'NMC', 'Citizens Advice')."
    )
    raw_analysis: str = Field(
        description="The detailed compliance reasoning and textual proof behind this classification."
    )