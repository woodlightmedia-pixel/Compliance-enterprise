import streamlit as st
import requests

# 💡 Import your new modular components
from components import render_header, render_delivery_preferences, display_triage_banner

# 1. Page Configuration
st.set_page_config(page_title="Workplace Dignity Control Plane", layout="wide")

# 2. Render Header Component
render_header()

# 3. Divide Layout into Main Interaction vs. System Telemetry Side Panel
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Case Analysis Portal")
    user_input = st.text_area(
        "Describe the scenario or incident with as much contextual detail as possible:",
        placeholder="e.g., During the team alignment sync, my supervisor made an explicit generalization...",
        height=150
    )
    
    st.markdown("---")
    
    # 📬 4. Render Delivery Preferences Component & capture form values
    preferences = render_delivery_preferences()

    # 5. Action Execution Trigger
    if st.button("🚀 Submit Case for Sequential Review"):
        if not user_input.strip():
            st.error("Please provide description text before triggering the multi-agent network.")
        elif preferences["send_personal"] and not preferences["req_email"].strip():
            st.error("Please supply a valid recipient email address for your personal reference copy.")
        elif preferences["send_comp"] and not preferences["comp_email"].strip():
            st.error("Please supply a valid compliance desk routing email address.")
        else:
            # Package up the payload using the variables from our component
            payload = {
                "message": {"parts": [{"text": user_input}]},
                "email_preferences": {
                    "send_to_requestor": preferences["send_personal"],
                    "requestor_email": preferences["req_email"],
                    "send_to_compliance": preferences["send_comp"],
                    "compliance_officer_email": preferences["comp_email"]
                }
            }
            
            with st.spinner("Anonymizing PII and running compliance models..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/api/v1/message/send", json=payload)
                    
                    if response.status_code == 200:
                        output_data = response.json()
                        
                        # 🛠️ ROBUST UNWRAPPING: Pull only the clean text out of the dictionary object
                        if isinstance(output_data, dict):
                            if "analysis" in output_data:
                                output_text = output_data["analysis"]
                            elif "text" in output_data:
                                output_text = output_data["text"]
                            else:
                                output_text = str(output_data)
                        else:
                            output_text = str(output_data)
                        
                        # Handle security guardrail blocks cleanly
                        if "automatically blocked by corporate data safety policies" in str(output_text).lower():
                            st.warning("⚠️ **Security Guardrail Active:** This scenario contains elements that violate corporate data governance policies. Processing has been halted.")
                            with st.expander("See Raw Security Log Details"):
                                st.code(str(output_text), language="json")
                        
                        # 🚀 Clean compliance scenario! Render the clean markdown report
                        else:
                            # 📊 Render Dynamic Alert Banner Component
                            display_triage_banner(output_text)
                            
                            st.markdown("### 📋 Generated Case Reference File")
                            st.markdown(output_text)  # This will render beautiful markdown text!
                            
                    else:
                        st.error(f"Platform Error: Guardrail barrier triggered. (Status {response.status_code})")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Connection Refused: Ensure your FastAPI backend server is running on port 8000!")

with col2:
    st.subheader("📊 System Telemetry")
    st.info("Core Engine: Google ADK 2.0")
    st.success("Platform Guardrails: Hardened Ingress/Egress Active")
    st.metric(label="Active Knowledge Frameworks", value="4 Files Configured")
    st.metric(label="Sequential Protocol Mode", value="A2A Private Mode")