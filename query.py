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
    n_results=1
)

for i, doc in enumerate(results["documents"][0]):
    print(f"{i+1}. {doc}\n")