import fitz
import chromadb
import uuid
from langchain_ollama import OllamaEmbeddings
from pathlib import Path

embeddings = OllamaEmbeddings(model="nomic-embed-text:latest", num_gpu=0)

client     = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="legal_docs")

def embed_in_batches(texts, batch_size=10):
    all_vecs = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        vecs  = embeddings.embed_documents(batch)
        all_vecs.extend(vecs)
        print(f"  Embedded {min(i+batch_size, len(texts))}/{len(texts)} pages")
    return all_vecs

def ingest_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texts, metas, ids = [], [], []
    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
        if len(text) > 100:
            texts.append(text[:1000])
            metas.append({
                "source": str(pdf_path),
                "page":   str(page_num)
            })
            ids.append(str(uuid.uuid4()))

    print(f"Embedding {len(texts)} pages from {pdf_path}...")
    vecs = embed_in_batches(texts)

    collection.add(
        ids=ids,
        embeddings=vecs,
        documents=texts,
        metadatas=metas
    )
    print(f"Indexed {len(texts)} pages from {pdf_path}")

if __name__ == "__main__":
    folder = Path("data/legal_docs")
    pdfs   = list(folder.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in data/legal_docs/")
    for pdf in pdfs:
        ingest_pdf(pdf)
    print("Ingestion complete")