import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import tarfile
import boto3

load_dotenv()
chroma_db_path = os.path.join(os.getcwd(), "chroma_db")
s3_bucket = "solidvessel-docs-embeddings"
repo_path = os.getenv("REPO_PATH")

def read_files_from_directory(file_extensions=(".md",)):
    print("Reading the files...")
    repo_data = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(file_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    repo_data[file_path] = f.read()
    return repo_data

def split_to_chunks():
    print("Splitting files into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_chunks = []
    for file_path, content in docs.items():
        chunks = splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            docs_chunks.append({"source": file_path, "chunk_id": i, "content": chunk})
    return docs_chunks

def add_embeddings(collection):
    print("Adding embeddings...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    for chunk in docs_chunks:
        embedding = client.embeddings.create(
            input=chunk["content"], model="text-embedding-3-small"
        ).data[0].embedding

        collection.add(
            documents=[chunk["content"]],
            metadatas=[{"source": chunk["source"], "chunk_id": chunk["chunk_id"]}],
            ids=[f"{chunk['source']}_{chunk['chunk_id']}"],
            embeddings=[embedding]
        )

def create_vector_db():
    print("Creating Vector DB...")
    vector_db = chromadb.PersistentClient(path=chroma_db_path)
    collection = vector_db.get_or_create_collection(name="solidvessel_docs")
    add_embeddings(collection)

def upload_to_s3():
    print("Uploading to S3...")
    s3_key = "chroma_db.tar.gz"
    tar_path = s3_key
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(chroma_db_path, arcname=os.path.basename(chroma_db_path))

    s3 = boto3.client("s3")
    s3.upload_file(tar_path, s3_bucket, s3_key)
    print(f"Uploaded {tar_path} to s3://{s3_bucket}/{s3_key}")

docs = read_files_from_directory()
docs_chunks = split_to_chunks()
create_vector_db()
if (os.getenv("UPLOAD_TO_S3")):
    upload_to_s3()
print("Done!")