# 🔎 ResearchLens — AI-Powered Research Paper Assistant

**ResearchLens** is a Retrieval-Augmented Generation (RAG) application that helps users explore research papers, retrieve relevant passages, and generate evidence-grounded answers to natural-language questions.

Instead of manually searching through lengthy PDFs, users can ask questions and receive contextual answers powered by semantic search and a Large Language Model (LLM).

## ✨ Features

- **PDF document loading:** Extract text and metadata from research papers.
- **Intelligent text chunking:** Split documents into manageable, overlapping chunks using LangChain.
- **Semantic embeddings:** Convert text into 384-dimensional vectors using `sentence-transformers/all-MiniLM-L6-v2`.
- **Vector similarity search:** Use FAISS to retrieve relevant passages based on a user's question.
- **LLM-powered answers:** Generate contextual responses using Groq-hosted language models.
- **Source metadata:** Retain source filenames and page information during retrieval.
- **REST API:** Expose question-answering functionality through FastAPI.
- **Interactive web interface:** Ask questions through a React frontend built with Vite.

## 🏗️ Architecture

```text
                Research Paper PDFs
                         |
                         v
                 PDF Text Extraction
                    (PyMuPDF)
                         |
                         v
                  Text Chunking
                   (LangChain)
                         |
                         v
                  Text Embeddings
              (Hugging Face Model)
                         |
                         v
                   FAISS Index
                         |
                         v
                  User's Question
                         |
                         v
                 Semantic Retrieval
                         |
                         v
                Retrieved Passages
                         |
                         v
                  Groq-hosted LLM
                         |
                         v
                 Generated Answer
                         |
                         v
                  React Frontend
```

## 🛠️ Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| RAG framework | LangChain |
| PDF processing | PyMuPDF |
| Embedding model | Sentence Transformers, `all-MiniLM-L6-v2` |
| Vector database/index | FAISS |
| Language model API | Groq |
| Environment configuration | Python dotenv |

## 📂 Project Structure

```text
research-lens/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag_test.py
│   │   ├── splitter_test.py
│   │   ├── embedding_test.py
│   │   ├── vector_store_test.py
│   │   ├── build_vector_store.py
│   │   ├── query_vector_store.py
│   │   └── ask_research.py
│   ├── data/
│   │   └── papers/
│   ├── vector_store/
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── index.html
├── .gitignore
└── README.md
```

*The structure above describes the main project components; local data, virtual environments, and generated index files should not necessarily be committed.*

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- A Groq API key
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd research-lens
```

Replace the placeholder with your repository's actual URL.

### 2. Set up the backend

```bash
cd backend
python3.12 -m venv venv312
source venv312/bin/activate
```

Install the backend dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own API key. Never commit this file or expose the key publicly.

### 3. Add research papers

Place the PDF files you are authorized to use inside:

```text
backend/data/papers/
```

Make sure the directory exists and contains the PDFs you want to index.

### 4. Build the vector store

From the `backend/` directory, run:

```bash
python app/build_vector_store.py
```

This processes the available PDFs, creates embeddings, builds the FAISS index, and saves the local vector store.

### 5. Start the backend API

From the `backend/` directory:

```bash
python -m uvicorn app.main:app --reload
```

The API will normally be available at:

- API root: `http://127.0.0.1:8000/`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

Keep the backend running while using the frontend.

### 6. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually:

`http://localhost:5173`

Ensure the FastAPI backend is running and configured to allow requests from the frontend origin.

## 💡 How It Works

1. **Document ingestion:** Research papers are loaded from PDF files.
2. **Chunking:** The text is divided into chunks of up to 1,000 characters, with 200 characters of overlap.
3. **Embedding generation:** Each chunk is converted into a numerical vector using the selected Sentence Transformers model.
4. **Indexing:** FAISS stores the vectors for similarity search.
5. **Retrieval:** When a user submits a question, the system retrieves relevant chunks from the saved index.
6. **Answer generation:** The retrieved context and question are passed to a Groq-hosted LLM through LangChain.
7. **Response delivery:** FastAPI returns the generated answer to the React interface.

## 🔐 Security and Data Handling

- Keep API keys in environment variables rather than source code.
- Exclude `.env`, virtual environments, caches, and other local secrets from Git.
- Only load FAISS pickle files that you created yourself or otherwise trust.
- Use research papers that you have permission to process and share.
- Do not publish confidential or copyrighted PDFs without authorization.

## 🗺️ Future Improvements

- [ ] Upload and index PDFs directly through the web interface.
- [ ] Display clickable source citations with accurate page references.
- [ ] Improve retrieval quality with metadata filtering and retrieval evaluation.
- [ ] Support comparisons across multiple research papers.
- [ ] Add conversation history and follow-up questions.
- [ ] Add document management and index refresh functionality.
- [ ] Deploy the frontend and backend for public access.

## 🎯 Project Goal

ResearchLens aims to make academic literature easier to navigate by combining semantic retrieval with LLM-based answer generation, helping users discover relevant information across research documents more efficiently.

---

**Built with React, FastAPI, LangChain, FAISS, Hugging Face, and Groq.**