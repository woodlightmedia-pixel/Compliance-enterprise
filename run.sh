#!/bin/bash

# Start the FastAPI backend in the background (using the & symbol)
uvicorn src.protocols.router:app --host 127.0.0.1 --port 8000 &

# Start the Streamlit frontend in the foreground on Cloud Run's default port (8080)
streamlit run src/ui/app.py --server.port 8080 --server.address 0.0.0.0