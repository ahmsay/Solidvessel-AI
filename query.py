import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

vector_db = chromadb.PersistentClient(path="./chroma_db")
collection = vector_db.get_or_create_collection(name="solidvessel_docs")

query = input("Enter your question: ")
query_embedding = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding], 
    n_results=5
)

combined_text = "\n".join([doc[0] for doc in results["documents"]])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You're an AI assistant that explains the project."},
        {"role": "user", "content": f"Based on these docs, answer the question:\n\n{query}\n\n{combined_text}"}
    ]
)

print("✅ AI-Expanded Answer:\n", response.choices[0].message.content)
