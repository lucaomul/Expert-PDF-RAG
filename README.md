# 📄 ChatPDF — Conversational RAG System for Document Intelligence

> Stop searching PDFs. Start querying them.

---

## 🚀 Overview

ChatPDF is an AI-powered document intelligence system that transforms static PDFs into **interactive, queryable knowledge bases**.

Instead of manually searching through large documents, users can ask natural language questions and receive **context-aware answers with exact source references**.

The system is built using a **Retrieval-Augmented Generation (RAG)** architecture to ensure accuracy, traceability, and reliability.

---

## 🧠 What It Does

* Converts PDFs into searchable semantic data
* Enables natural language querying over documents
* Returns answers with **exact page-level source attribution**
* Supports follow-up questions with conversational context

---

## ⚙️ Core Features

### 🔍 Semantic Search (RAG)

* Uses embeddings + vector search to retrieve relevant document chunks
* Eliminates reliance on keyword-based search (Cmd+F limitations)

### 💬 Conversational Memory

* Maintains context across multiple queries
* Enables natural multi-step interactions with documents

### 📌 Source Attribution

* Every response includes the **exact page reference**
* Improves trust and verifiability of AI-generated answers

### 🔒 Privacy-Focused

* Documents are processed and indexed locally
* No external storage of sensitive data

### 🎨 Custom UI

* Built with Streamlit
* Includes dynamic UI controls for user customization

---

## 🧪 Use Cases

### 🎓 Students

* Summarize large study materials
* Generate quick explanations for complex topics
* Self-test using document-based Q&A

### 💼 HR & Recruiters

* Analyze multiple CVs simultaneously
* Extract candidate insights instantly
* Compare skills and experience across applicants

### ⚖️ Legal & Business

* Extract key clauses (termination, payment, risks)
* Reduce contract review time from hours to minutes

### 🧑‍💻 Technical Users

* Navigate large documentation (APIs, manuals)
* Retrieve specific technical details instantly

---

## 🛠️ Tech Stack

* **Python**
* **OpenAI API (GPT-4o)**
* **Vector Search (Embeddings-based retrieval)**
* **Streamlit (UI)**
* **Document Processing Pipelines**

---

## ⚡ How It Works

1. Upload PDF documents
2. Extract and chunk text data
3. Convert text into embeddings
4. Store in vector database
5. Retrieve relevant chunks based on query
6. Generate answer using LLM + retrieved context

---

## ▶️ Getting Started

### Install dependencies

```bash id="x8k3pl"
pip install -r requirements.txt
```

### Configure API key

```python id="l9f2qw"
OPENAI_API_KEY = "your_key_here"
```

### Run the app

```bash id="p2m8zn"
streamlit run app.py
```

---

## 📈 Why This Matters

Traditional document search:

* relies on keyword matching
* lacks context awareness
* is time-consuming

ChatPDF:

* enables **semantic understanding**
* provides **traceable answers**
* transforms documents into **interactive systems**

---

## 🔮 Future Improvements

* Multi-document cross-referencing
* Persistent vector database storage
* Advanced filtering (by section, topic, metadata)
* Performance optimization for large-scale document sets
* Integration with external knowledge sources

---

## 👤 Author

**Luca Craciun**
AI Automation Engineer

GitHub: https://github.com/lucaomul
LinkedIn: https://www.linkedin.com/in/gabriel-luca-craciun-25ba95295

---

## ⭐ If you find this useful

Star the repo or fork it to build your own document intelligence system.
