from langchain_core.documents import Document
from clone import get_files
from llm import get_llm
from vector_db import get_vector_store


def generate_descriptions():
    vector_store = get_vector_store()
    llm = get_llm()

    files = get_files()
    for file in files:
        with open(file, "r",encoding="UTF-8") as f:
            print(f"Generating description for {file}")
            text = f.read()
            messages = [
                (
                    "system",
                    "You are a code description generator. Given a file name and its content, generate a descriptive summary of the code's purpose and functionality. The description should be detailed enough to allow retrieval based on natural language queries. For example, if the code is a middleware function in Node.js, generate a description like 'This code implements middleware for a Node.js application.",
                ),
                (
                    "human",
                    f"Please generate a description for the following code snippet: \n filename: {file} \n code: {text}",
                ),
            ]
            response = llm.invoke(messages)
            print(file)
            print()
            vector_store.add_documents(
                [
                    Document(
                        id=file,
                        page_content=str(response.content),
                        metadata={"filename": file},
                    )
                ]
            )


if __name__ == "__main__":
    generate_descriptions()
