import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
#import re
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

def read_files_from_directory(directory, file_extensions=(".md")):
    repo_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extensions):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    repo_data[file_path] = f.read()
    return repo_data

#def strip_markdown(md_text):
#    md_text = re.sub(r"!\[.*?\]\(.*?\)", "", md_text)  # Remove images
#    md_text = re.sub(r"\[.*?\]\(.*?\)", "", md_text)  # Remove links
#    md_text = re.sub(r"`([^`]*)`", r"\1", md_text)  # Remove inline code formatting
#    md_text = re.sub(r"#{1,6}\s*", "", md_text)  # Remove headings
#    md_text = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", md_text)  # Remove bold/italic
#    return md_text.strip()

repo_path = "../Solidvessel"
docs = read_files_from_directory(repo_path)
#cleaned_docs = [strip_markdown(doc) for doc in docs]

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_chunks = []
for file_path, content in docs.items():
    chunks = splitter.split_text(content)
    for i, chunk in enumerate(chunks):
        docs_chunks.append({"source": file_path, "chunk_id": i, "content": chunk})

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
vector_db = chromadb.PersistentClient(path="./chroma_db")

collection = vector_db.get_or_create_collection(name="solidvessel_docs")

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