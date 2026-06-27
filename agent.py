from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from tools import search_legal_docs, search_web

llm = ChatOllama(model="mistral:latest", temperature=0,num_gpu=0)

@tool
def search_legal_docs_tool(query: str) -> str:
    """Search internal Indian legal corpus — BNS, IPC, BNSS documents.
    Use this FIRST for any legal query."""
    return search_legal_docs(query)

@tool
def search_web_tool(query: str) -> str:
    """Search web for Indian legal information.
    Use ONLY if search_legal_docs returns no relevant results."""
    return search_web(query)

agent = create_agent(
    model=llm,
    tools=[search_legal_docs_tool, search_web_tool],
    system_prompt=(
        "You are an Indian legal assistant. "
        "Always search legal documents first. "
        "Cite source and page number in your answer. "
        "If not found locally, search the web."
    )
)

def run_agent(query: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content