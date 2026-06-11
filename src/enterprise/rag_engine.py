# src/enterprise/rag_engine.py
import os
from google import genai
import pinecone

# Initialize clients
client = genai.Client()
pc = pinecone.Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# 🛠️ MATCHING UPDATES: Point queries to the v2 space using the new model
INDEX_NAME = "compliance-knowledge-base-v2"
index = pc.Index(INDEX_NAME)

def retrieve_compliance_context(user_scenario: str) -> str:
    # Generate the 3072-dimension lookup coordinate vector
    embedding_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=user_scenario
    )
    query_vector = embedding_response.embeddings[0].values
    
    # Query your updated high-dimension index
    results = index.query(
        vector=query_vector, 
        top_k=3, 
        include_metadata=True
    )
    
    context_chunks = [match['metadata']['text'] for match in results['matches'] if 'text' in match['metadata']]
    return "\n\n".join(context_chunks)