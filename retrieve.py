import chromadb
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

client     = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="legal_docs")

def retrieve(query, top_k=4):
    query_vec = embeddings.embed_query(query)
    results   = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    docs  = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": docs[i], "metadata": metas[i]}
            for i in range(len(docs))]