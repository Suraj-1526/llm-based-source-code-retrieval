import getpass
import os
from langchain_cohere.embeddings import CohereEmbeddings
from cohere import Client
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("COHERE_API_KEY"):
    os.environ["COHERE_API_KEY"] = getpass.getpass("Enter your Cohere API key: ")


cohere_client = Client(os.getenv("COHERE_API_KEY"))

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    client=cohere_client,
    async_client=None,
)


def get_embeddings():
    return embeddings
