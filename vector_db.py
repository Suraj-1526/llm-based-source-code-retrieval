from langchain_chroma import Chroma

import getpass
import os

from pinecone import Pinecone, ServerlessSpec
from embedding_model import get_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()
embeddings = get_embeddings()


if not os.getenv("PINECONE_API_KEY"):
    os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")

pinecone_api_key = os.environ.get("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_api_key)


import time

index_name = "descriptions"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)


vector_store = PineconeVectorStore(index=index, embedding=embeddings)


def get_vector_store():
    return vector_store

def get_retriever():
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    return retriever