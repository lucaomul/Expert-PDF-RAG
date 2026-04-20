# 📄 ChatPDF — Conversational Document Intelligence

A retrieval-augmented generation (RAG) system that turns PDFs into **interactive, context-aware knowledge systems** — with semantic search, conversational memory, and source-grounded answers.

> Built because Ctrl+F doesn’t understand context, and LLMs without retrieval hallucinate confidently.

---

## 🎬 Demo

![Demo](./docs/RAG_ChatPDF.gif)

---

## 🧠 How It Works

```
PDF Upload → Text Extraction → Chunking → Embedding → ChromaDB
                                                           ↓
User Query → History-Aware Query Rewriting → Vector Search
                                                           ↓
                                 GPT-4o → Answer + Source Context
```

**The pipeline:**

1. PDFs are parsed and split into overlapping chunks
2. Each chunk is embedded and stored in ChromaDB (local vector DB)
3. User query is rewritten into a **standalone question** using chat history
4. Relevant chunks are retrieved via semantic similarity
5. GPT-4o generates an answer using retrieved context
6. Sources (file + page) are returned for transparency

---

## ⚙️ Key Design Decisions

* **Why ChromaDB?**
  Runs fully local — no external infra, no data leakage. Ideal for sensitive PDFs (contracts, internal docs, research).

* **Why overlapping chunks?**
  Prevents context loss at chunk boundaries. Without overlap, answers degrade fast on long paragraphs.

* **Why history-aware retrieval?**
  This is the major upgrade vs basic RAG.
  Instead of querying raw input, the system rewrites it into a **context-aware standalone query**.

  👉 Enables:

  * follow-up questions
  * conversational flow
  * significantly better retrieval accuracy

* **Why not LangChain 1.x?**
  The project uses:

  * `create_history_aware_retriever`
  * `create_retrieval_chain`

  These are removed in 1.x. Migrating would require a full LCEL/LangGraph rewrite with no real gain for this use case.

  👉 Decision: **use stable, expressive abstractions instead of overengineering**

* **Why Streamlit UI?**
  Fastest way to build a usable interface. Focus stays on RAG logic, not frontend complexity.

---

## 📊 What Changed vs Basic RAG

Compared to a standard "PDF QA" system:

* ➕ Added **chat memory**
* ➕ Added **query rewriting (history-aware retriever)**
* ➕ Added **multi-document support**
* ➕ Added **source tracking (file + page)**
* ➕ Built a **custom terminal-style UI**

👉 Result: transforms a simple QA tool into a **conversational document system**

---

## 🛠️ Tech Stack

* **Python 3.12**
* **OpenAI API** — GPT-4o (generation) + embeddings
* **ChromaDB** — local vector database
* **LangChain (0.3.x)** — RAG orchestration
* **Streamlit** — UI layer
* **PyPDFLoader** — PDF parsing

---

## ▶️ Getting Started

```bash
git clone https://github.com/lucaomul/chatpdf.git
cd chatpdf

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Set your API key:

```env
OPENAI_API_KEY=your_key_here
```

Run:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ChatPDF/
├── app.py              # Streamlit UI + RAG orchestration
├── requirements.txt
├── RAG_ChatPDF.gif     # Demo preview
```

---

## 🧪 Use Cases

**Legal & Contracts** — Extract clauses instantly
→ "What are the termination conditions?"

**Technical Docs** — Navigate large documentation
→ "How is authentication handled?"

**Research Papers** — Summarize and cross-reference
→ "What is the main contribution of this paper?"

**General Knowledge Bases** — Turn any PDF into a chatbot

---

## ⚠️ Limitations

* In-memory vector store (data not persisted)
* Dependent on OpenAI API
* Not optimized for very large datasets

---

## 🔮 What's Next

* Persistent vector database
* Streaming responses
* PDF highlighting (exact text spans)
* Hybrid search (BM25 + embeddings)
* Migration to LangChain 1.x (LCEL)

---

## 👤 Author

**Luca Crăciun** — AI Automation Engineer
GitHub: https://github.com/lucaomul
LinkedIn: https://www.linkedin.com/in/gabriel-luca-craciun-25ba95295

---

## 🧩 Final Note

This isn’t just a demo.

It’s a practical implementation of RAG focused on:

* correctness
* usability
* real-world workflows

---
