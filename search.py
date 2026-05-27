from vector_db import get_retriever


def init():
    retriever = get_retriever()
    print("Loading vector store...")
    print("---Type 'exit' to quit.---")
    while True:
        query = input("Enter a query: ")
        if query == "":
            continue
        if query == "exit":
            break
        docs = retriever.invoke(query)
        for doc in docs:
            print(doc.metadata["filename"])


if __name__ == "__main__":
    print("--- Welcome to the code search engine!---")
    init()
