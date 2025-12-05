# 🎬 YouTube Transcript Chatbot (RAG Powered)

Ask questions about **any YouTube video** just by pasting a link — the chatbot retrieves, processes, and understands the transcript using **Retrieval-Augmented Generation (RAG)**.

🚀 Live Demo: *(Add your deployed link here)*  
📦 Backend: FastAPI (Render)  
🎨 Frontend: React + Tailwind (Vercel)

---

## 🧠 Features

| Feature | Description |
|--------|------------|
| 🔍 YouTube URL → Transcript Extraction | Automatically fetches and extracts captions based on the video ID |
| 🌍 Supports Multi-Language Videos | Detects non-English transcripts and translates them |
| 🧩 Smart Chunking | Splits transcript into semantically meaningful sections |
| 📚 RAG-Powered Question Answering | Queries embedding-based vector store to answer accurately |
| ⚡ Caching | Transcript + embeddings processed only once per video |
| 💬 Premium Chat UI | Modern assistant-style interface with streaming UX |
| ☁ Fully Deployed | Backend on Render, Frontend on Vercel |

---

<img width="2865" height="1497" alt="Screenshot 2025-12-05 210351" src="https://github.com/user-attachments/assets/010ba4ba-54be-45c4-9caa-27b85b264da8" />

<img width="2876" height="1541" alt="Screenshot 2025-12-05 194425" src="https://github.com/user-attachments/assets/5c98fa23-9651-4863-bb60-565273952226" />


## 🏗️ Architecture

  ┌───────────────────────┐
  │       Frontend        │
  │ React + Tailwind UI   │
  └───────────┬───────────┘
              │ (REST API)
              ▼
   ┌──────────────────────────┐
   │         Backend          │
   │ FastAPI + LangChain RAG │
   └──────────────────────────┘
              │
              ▼
  ┌──────────────────────────┐
  │ Vector Store (Embeddings)│
  └──────────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Groq / Qwen Model   │
    │ + Proxy Transcript  │
    └─────────────────────┘

---

## 🛠️ Tech Stack

### 🔹 Backend
- Python 3.11
- FastAPI
- LangChain
- Vector Embeddings
- Groq / Qwen model
- YouTube Transcript API (+ proxy support)
- `lru_cache` for performance

### 🔹 Frontend
- React (Vite)
- TailwindCSS
- Fetch-based API integration
- Animated Chat UI

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repo

```sh
git clone https://github.com/your-username/youtube-rag-chatbot.git
cd youtube-rag-chatbot
