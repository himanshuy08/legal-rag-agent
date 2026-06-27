# Legal RAG Agent 🏛️

An **Agentic RAG system** for querying Indian legal documents — BNS 2023, IPC 1860, and BNSS 2023 — using a ReAct agent that dynamically decides between local vector search and live web search to answer legal queries with cited sources.

---

## Demo

> **Query:** "What is the punishment for murder under BNS 2023?"
> 
> **Agent:** Searches ChromaDB → Retrieves BNS Section 101 → Generates grounded answer with page citation.

---

## Architecture
User Query

│

▼

LangChain ReAct Agent (Mistral via Ollama)

│

├──► Tool 1: search_legal_docs

│         └── OllamaEmbeddings (nomic-embed-text)

│         └── ChromaDB Vector Store

│         └── Hybrid Retrieval (Dense + BM25)

│         └── Returns: cited chunks with source + page

│

└──► Tool 2: search_web (fallback)

└── DuckDuckGo Search

└── Used when local corpus insufficient

---

## Features

- **Agentic decision making** — agent selects retrieval tool at runtime based on query
- **Local-first retrieval** — ChromaDB dense retrieval over 700+ pages of Indian law
- **Web search fallback** — DuckDuckGo triggered when local corpus insufficient
- **Source citation** — every answer includes source document + page number
- **Fully local** — no OpenAI API, no cloud dependency, runs on-device via Ollama
- **Gradio UI** — browser-based interface for querying

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | LangChain + LangGraph ReAct |
| LLM | Mistral-7B via Ollama |
| Embeddings | nomic-embed-text via Ollama |
| Vector Store | ChromaDB (persistent) |
| Web Search | DuckDuckGo (no API key needed) |
| UI | Gradio |

---

## Legal Corpus

| Document | Pages |
|---|---|
| Bharatiya Nyaya Sanhita (BNS) 2023 | ~200 |
| Indian Penal Code (IPC) 1860 | ~300 |
| Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 | ~297 |

---

## Project Structure
legal-rag-agent/

├── data/

│   └── legal_docs/        # BNS, IPC, BNSS PDFs

├── chroma_storage/        # Persistent vector index

├── ingest.py              # PDF parsing + embedding + indexing

├── retrieve.py            # ChromaDB retrieval

├── tools.py               # Agent tools (local search + web)

├── agent.py               # LangChain ReAct agent

├── app.py                 # Gradio UI

└── requirements.txt

---

## Setup and Run

**1. Clone the repo**
```bash
git clone https://github.com/himanshuy08/legal-rag-agent.git
cd legal-rag-agent
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Pull Ollama models**
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

**5. Add legal PDFs to `data/legal_docs/`**

Download free official PDFs:
```bash
# BNS 2023
curl -L "https://www.mha.gov.in/sites/default/files/250883_english_01042024.pdf" -o data/legal_docs/BNS_2023.pdf

# IPC 1860
curl -L "https://www.indiacode.nic.in/bitstream/123456789/11091/1/the_indian_penal_code,_1860.pdf" -o data/legal_docs/IPC_1860.pdf

# BNSS 2023
curl -L "https://prsindia.org/files/bills_acts/bills_parliament/2023/Bharatiya_Nagarik_Suraksha_Sanhita,_2023.pdf" -o data/legal_docs/BNSS_2023.pdf
```

**6. Ingest documents**
```bash
python ingest.py
```

**7. Run the app**
```bash
python app.py
```

Open `http://127.0.0.1:7860` in your browser.

---

## Example Queries

**Local corpus (BNS/IPC/BNSS):**
What is the punishment for murder under BNS 2023?

What is Section 302 of IPC?

What are bailable and non-bailable offences?

What is a cognizable offence under BNSS?

**Web search fallback:**
What is the latest Supreme Court judgment on Article 370?

What is the current status of sedition law in India?

---

## How It Works

1. User submits a legal query via Gradio UI
2. ReAct agent receives the query and reasons about which tool to use
3. **Tool 1 — `search_legal_docs`:** Embeds query with `nomic-embed-text` → queries ChromaDB → returns top-4 chunks with source + page
4. **Tool 2 — `search_web`:** Falls back to DuckDuckGo if local search insufficient
5. Mistral generates a grounded answer with citations
6. Answer displayed in UI

---

## Requirements
Python 3.10+

Ollama installed and running locally

---

## Author

**Himanshu** — M.Tech (IT - Data Analytics), NIT Jalandhar  
[GitHub](https://github.com/himanshuy08)
