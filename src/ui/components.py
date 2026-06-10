import streamlit as st

def render_header():
    """Renders a clean, corporate header configuration for the platform."""
    st.title("💼 Internal Workplace Dignity & Compliance Workspace")
    st.markdown("---")

def render_delivery_preferences():
    """Renders the secure transactional email delivery checkboxes and inputs.
    Returns a dictionary containing the active configuration values.
    """
    st.subheader("📬 Secure Delivery Preferences")
    col_req, col_comp = st.columns(2)
    
    with col_req:
        send_personal = st.checkbox("Email me a personal copy for my reference", value=False)
        req_email = st.text_input(
            "Your Email Address", 
            placeholder="your.name@company.com", 
            disabled=not send_personal
        )

    with col_comp:
        send_comp = st.checkbox("Escalate and forward directly to the allocated Compliance Officer", value=False)
        comp_email = st.text_input(
            "Compliance Officer Email Destination", 
            placeholder="compliance-team@company.com", 
            disabled=not send_comp
        )
        
    st.markdown("---")
    
    return {
        "send_personal": send_personal,
        "req_email": req_email,
        "send_comp": send_comp,
        "comp_email": comp_email
    }

def display_triage_banner(output_text: str):
    """Parses the multi-agent execution output string and injects the correct
    contextual Streamlit status indicator banner.
    """
    if "[🚨 IMMEDIATE ACTION REQUIRED]" in output_text:
        st.error("🚨 Critical Priority Escalation Activated")
    elif "[MEDIUM SEVERITY]" in output_text:
        st.warning("⚠️ Standard Regulatory Grievance Review Triggered")
    else:
        st.info("ℹ️ Local/Informal Resolution Pathway Established")