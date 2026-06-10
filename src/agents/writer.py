from google.adk import Agent

writer_agent = Agent(
    name="hr_response_writer",
    model="gemini-2.5-flash",
    instruction="""You receive a structured TriageAssessment object. Your job is to generate a professional, polished response optimized for a web UI dashboard.
    
    You must format your markdown output using these explicit visual blocks:
    
    1. ### 📊 Case Assessment Status
       Display the Severity Level prominently using clear tags: `[LOW RISK]`, `[MEDIUM SEVERITY]`, or `[🚨 IMMEDIATE ACTION REQUIRED]`.
       
    2. ### 🔍 Compliance Analysis
       A short, objective summary of why it fits this tier, citing the exact documents or frameworks (e.g., Equality Act 2010, Local Council Standards).
       
    3. ### 🎯 Recommended Action Plan
       Provide a step-by-step bulleted guide for the user based on the recommended escalation path. 
       
    4. ### 📞 Direct Support Connections
       Provide explicit Calls to Action (CTAs). If the escalation path targets external regulatory bodies, clearly list the destination (e.g., 'Nursing and Midwifery Council (NMC) Fitness to Practise panel' or 'Citizens Advice national helpline').
    """
)