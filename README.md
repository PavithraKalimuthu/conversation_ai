# 🤖 Conversational AI Application

A production-style Conversational AI application built using FastAPI, Streamlit, Groq Llama 3.1, MySQL, MongoDB, ChromaDB, and HuggingFace Embeddings.

---

## Features

- Multi-user Login & Registration
- Conversational AI using Groq Llama 3.1
- Chat History Management (MySQL)
- Long-Term Memory (MongoDB)
- Retrieval-Augmented Generation (RAG) using ChromaDB
- PDF & Text Document Upload
- Streaming AI Responses
- Clean Streamlit User Interface
- Modular Project Architecture
- Logging Support

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq Llama 3.1 |
| Database | MySQL |
| Memory | MongoDB |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace Sentence Transformers |
| Language | Python |

---

## Project Structure

```
Conversational_AI/
│
├── app.py
├── main.py
├── config.py
├── database.py
├── auth.py
├── prompts.py
├── llm.py
├── memory_manager.py
├── rag_manager.py
├── orchestrator.py
├── utils.py
├── logger.py
├── requirements.txt
├── README.md
├── .env
│
├── uploads/
├── knowledge/
├── chroma_db/
└── logs/
```

---

## Installation

```bash
git clone https://github.com/<YOUR_USERNAME>/Conversational-AI.git

cd Conversational-AI

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

```env
GROQ_API_KEY=YOUR_API_KEY

MODEL_NAME=llama-3.1-8b-instant

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=conversation_ai

MONGO_URI=mongodb://localhost:27017

CHROMA_PATH=chroma_db

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## Run FastAPI

```bash
uvicorn main:app --reload
```

---

## Run Streamlit

```bash
streamlit run app.py
```

---

## API Endpoints

| Method | Endpoint |
|----------|----------|
| POST | /register |
| POST | /login |
| POST | /chat |
| POST | /upload |
| GET | /history/{user_id} |
| GET | /health |

---

## Future Enhancements

- JWT Authentication
- Cloud Database Integration
- Docker Deployment
- Role-Based Access
- Conversation Summarization
- Semantic Memory Search
- Multi-Agent Support

---

## Author

**Pavithra Kalimuthu**

AI | GenAI | Machine Learning | FastAPI | Streamlit | RAG | LLM