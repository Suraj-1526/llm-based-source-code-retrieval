
import getpass
import os
from langchain_sambanova import ChatSambaNova
from dotenv import load_dotenv 
load_dotenv()

if not os.getenv("SAMBANOVA_API_KEY"):
    os.environ["SAMBANOVA_API_KEY"] = getpass.getpass(
        "Enter your SambaNova Cloud API key: "
    )


llm = ChatSambaNova(
    model="Meta-Llama-3.3-70B-Instruct",
    max_tokens=512,
    temperature=0.7,
    top_p=0.01,
)

def get_llm():
    return llm