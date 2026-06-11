import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 🛠️ FIXED: Go inside the specific router file to pull out the direct APIRouter instance variable
from src.protocols.router import router 

# override=False ensures that real cloud secrets take strict priority over file placeholders
load_dotenv(override=False)

# Initialize the primary API server engine
app = FastAPI(
    title="Workplace Dignity & Compliance Multi-Agent Engine",
    description="Automated sequential compliance agent pipeline leveraging Google ADK 2.0",
    version="2.0.0"
)

# Configure local frontend connection access (CORS Guardrails)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 This line will now connect perfectly because 'router' is now a valid APIRouter object!
app.include_router(router)

@app.get("/")
def home_health_check():
    return {
        "status": "healthy",
        "engine": "Google ADK 2.0 Engine Active"
    }
