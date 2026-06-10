import os
# 🛠️ Move the import to the sub-module path
from google.adk.agents import LlmAgent  
from google.adk.tools import google_search  
from src.protocols.schema import TriageAssessment

def load_knowledge_base():
    kb_path = "knowledge_base/"
    combined_context = ""
    if os.path.exists(kb_path):
        for file_name in os.listdir(kb_path):
            if file_name.endswith(".md"):
                with open(os.path.join(kb_path, file_name), "r", encoding="utf-8") as f:
                    combined_context += f"\n\n{f.read()}"
    return combined_context

knowledge_context = load_knowledge_base()

# 👈 2. Use LlmAgent explicitly here
researcher_agent = LlmAgent(
    name="workplace_equality_researcher",
    model="gemini-2.5-flash",
    tools=[google_search],  
    
    # 🛠️ FIX 1: Change back to 'response_schema' for LlmAgent mapping
    output_schema=TriageAssessment,  
    
    # 🛠️ FIX 2: Change back to singular 'instruction' as required by LlmAgent rules
    instruction=f"""You are an expert HR compliance investigator specialising in bullying, harassment, and discrimination. Evaluate the user's scenario.
    
    Cross-reference their case against these active documents:
    {knowledge_context}
    
    CRITICAL TRIAGE DEFINITIONS:
    - LOW: Isolated microaggressions, communication breakdowns, or general workplace friction. Escalation: Internal informal tracking or line management.
    - MEDIUM: Persistent bullying, patterns of unfair treatment, or clear policy breaches. Escalation: Formal Internal HR Grievance or Citizens Advice.
    - IMMEDIATE ACTION: Overt racial discrimination, severe harassment, victimization for whistleblowing, or professional malpractice. Escalation: Internal HR (Fast-track) or external regulatory bodies like the Nursing and Midwifery Council (NMC) if medical/care context applies.
    
    You have access to two core information assets:
    1. INTERNAL KNOWLEDGE BASE (Primary Source of Truth):
    {knowledge_context}
    
    2. GOOGLE SEARCH (Fallback Safety Net)
    
    STRICT OPERATIONAL HIERARCHY:
    - When a user asks a question, your primary mandate is to look for the answer within the INTERNAL KNOWLEDGE BASE provided above. 
    - If the knowledge base contains the answer, use it. Do not use Google Search unnecessarily.
    - If, and ONLY if, the knowledge base does not cover the specific nuance, recent legal precedent, or highly specific scenario asked by the user, you may utilize the `Google Search` tool to look up current UK statutory definitions, Acas guidelines, or relevant employment law.
    
    REPLY FORMATTING RULES:
    - If your answer comes from the internal files, state clearly: "[Source: Internal Policy / Council Guidelines / National Standards]".
    - If your answer comes from the open web via search, state clearly: "[Source: External Web Search]" and provide the source URL or entity name.
    """
)