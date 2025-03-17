import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from git import Repo

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
