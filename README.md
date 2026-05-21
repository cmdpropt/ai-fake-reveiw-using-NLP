# 🤖 IT Help Desk Chatbot — RAG + Agentic AI

> AI-powered first-line IT support system built using Retrieval-Augmented Generation and agentic AI frameworks. Developed in collaboration with IIT Kanpur (March 2026).

---

## 📌 What It Does

Automates L1 IT support queries end-to-end — no human needed for common issues.

- Accepts user query in natural language
- Classifies query type (hardware / software / network / account)
- Retrieves relevant knowledge base chunks via RAG
- Generates accurate, context-aware response
- Escalates unresolved queries to human agent automatically

> Reduced average first-response time from ~8 min to ~2 min in simulated enterprise environment (~75% reduction in manual L1 effort)

---

## 🧠 How It Works

```
User Query
    │
    ▼
Query Classifier (NLP)
    │
    ▼
Vector Store Retrieval (RAG)
    │
    ▼
LLM Response Generator
    │
    ├──► Resolved? → Return Answer to User
    │
    └──► Unresolved? → Escalate to Human Agent
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| AI Framework | RAG (Retrieval-Augmented Generation) |
| NLP | Hugging Face Transformers |
| Vector Store | FAISS |
| Agentic Layer | Custom agentic pipeline |
| Backend | FastAPI |

---

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.10
pip
```

### Installation
```bash
git clone https://github.com/cmdpropt/it-helpdesk-rag
cd it-helpdesk-rag
pip install -r requirements.txt
```

### Run
```bash
python app.py
```
Visit `http://localhost:8000` in your browser.

---

## 📁 Project Structure

```
it-helpdesk-rag/
├── app.py                  # Main entry point
├── rag_pipeline.py         # RAG retrieval + generation logic
├── classifier.py           # Query classification module
├── knowledge_base/         # IT support documents & FAQs
├── vector_store/           # FAISS index
├── requirements.txt
└── README.md
```

---

## 🤝 Collaboration

Built as part of a collaborative project with **IIT Kanpur** (March 2026) focused on enterprise IT automation using modern AI frameworks.


## ⚠️ Disclaimer

This project was developed in a **simulated enterprise environment** for educational and research purposes. No real user data was used or stored.


## 📬 Contact

**Saksham Awasthi** — [LinkedIn](https://www.linkedin.com/in/saksham-awasthi-4267b0254/) | [GitHub](https://github.com/cmdpropt)
