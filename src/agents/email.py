import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.adk import Agent

# 🛠️ Define the Python tool the agent uses to physically interact with the mail server
def send_secure_email(to_address: str, subject: str, html_body: str) -> str:
    """Uses the environment configuration to securely dispatch an email via SMTP."""
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SMTP_SENDER_EMAIL")
    sender_password = os.getenv("SMTP_SENDER_PASSWORD") # Secure app password
    
    if not sender_email or not sender_password:
        return "Email tool simulation active: SMTP credentials missing from .env"
        
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Workplace Dignity Platform <{sender_email}>"
        msg["To"] = to_address
        
        part = MIMEText(html_body, "html")
        msg.attach(part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_address, msg.as_string())
        return f"Successfully dispatched email to {to_address}"
    except Exception as e:
        return f"Failed to deliver email to {to_address} due to error: {str(e)}"


# 🤖 Create the Google ADK Email Agent
email_agent = Agent(
    name="email_dispatcher_agent",
    model="gemini-2.5-flash",
    tools=[send_secure_email],
    instruction="""You are a secure, automated corporate communications dispatcher. 
    You receive:
    1. A final, polished Markdown compliance report.
    2. Email delivery preferences (destination addresses and permission flags).
    
    YOUR MANDATE:
    - Check the delivery flags. If `send_to_requestor` is True, clean up the markdown report into a structured, clear, and reassuring plain HTML body. Subject line should be: "Confidential: Your Workplace Review Summary & Recommended Actions".
    - If `send_to_compliance` is True, compile a concise operational brief containing the case classification details, frameworks violated, and immediate action triggers. Address it directly to the designated compliance officer or system queue. Subject line should be: "URGENT: Compliance Review Required - [Triage Classification Flag]".
    
    SECURITY GUARDRAIL:
    Never log or leak the content of these emails to any open system console output. Call the `send_secure_email` tool strictly for active addresses.
    """
)