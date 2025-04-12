import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv
import boto3
import tarfile
import json

load_dotenv()

s3 = boto3.client('s3')
s3_bucket = "solidvessel-docs-embeddings"
s3_key = "chroma_db.tar.gz"
working_dir = "."
s3.download_file(s3_bucket, s3_key, working_dir)
with tarfile.open(".", 'r:gz') as tar:
    tar.extractall(path=working_dir)

vector_db = chromadb.PersistentClient(path="./chroma_db")
collection = vector_db.get_or_create_collection(name="solidvessel_docs")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def lambda_handler(event, context):
    query = event["body"]
    query_embedding = client.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=5
    )

    combined_text = "\n".join([doc[0] for doc in results["documents"]])

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that answers questions strictly related to this project. "
                "If the user asks something unrelated, refuse to answer and be sarcastic."
            )},
            {"role": "user", "content": f"Based on these docs, answer the question:\n\n{query}\n\n{combined_text}"}
        ]
    )

    return {
        'answer': json.dumps(response.choices[0].message.content)
    }
