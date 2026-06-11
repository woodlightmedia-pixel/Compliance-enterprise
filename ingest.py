# ingest.py
import os
import time
from google import genai
import pinecone

# Initialize clients
client = genai.Client()
pc = pinecone.Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# 🛠️ UPDATED: Shifted to version 2 to hold the larger vector space cleanly
INDEX_NAME = "compliance-knowledge-base-v2"

# Check if the database index actually exists in your cloud account
existing_indexes = [index.name for index in pc.list_indexes()]

if INDEX_NAME not in existing_indexes:
    print(f"🏗️ Index '{INDEX_NAME}' not found. Provisioning clean serverless instance...")
    
    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,  # 🔥 UPDATED: gemini-embedding-001 produces exactly 3072 dimensions
        metric="cosine", 
        spec=pinecone.ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    
    print("⏳ Waiting for Pinecone boot sequence to complete...")
    time.sleep(15) # Give the cloud routers an extra moment to map the larger space

# Connect to the high-dimension index
index = pc.Index(INDEX_NAME)

def ingest_knowledge_base():
    kb_path = "knowledge_base/"
    if not os.path.exists(kb_path):
        print("❌ Knowledge base directory not found.")
        return

    for file_name in os.listdir(kb_path):
        if file_name.endswith(".md"):
            with open(os.path.join(kb_path, file_name), "r", encoding="utf-8") as f:
                text_content = f.read()
            
            print(f"🧠 Generating embeddings for {file_name}...")
            # 🛠️ UPDATED: Swapped deprecated model out for the official modern replacement
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text_content
            )
            vector = response.embeddings[0].values
            
            # Upsert into Pinecone
            index.upsert(vectors=[{
                "id": file_name,
                "values": vector,
                "metadata": {"text": text_content}
            }])
    print("🚀 Ingestion complete! Pinecone v2 index is now populated.")

if __name__ == "__main__":
    ingest_knowledge_base()