from embedding_model import get_embeddings


embed = get_embeddings()
print(embed.embed_query("hello world"))
