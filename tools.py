import os
from retrieve import retrieve
from langchain_community.tools import DuckDuckGoSearchRun

ddg = DuckDuckGoSearchRun()

def search_legal_docs(query: str) -> str:
    """Search internal legal document corpus."""
    chunks = retrieve(query, top_k=4)
    if not chunks:
        return "No relevant information found in legal documents."
    result = ""
    for i, c in enumerate(chunks):
        source = c["metadata"].get("source", "unknown")
        page   = c["metadata"].get("page", "?")
        result += f"[Source: {source}, Page: {page}]\n{c['text']}\n\n"
    return result.strip()

def search_web(query: str) -> str:
    """Search web for legal information not in local corpus."""
    try:
        return ddg.run(query + " India law legal")
    except Exception as e:
        return f"Web search failed: {str(e)}"