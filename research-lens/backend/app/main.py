
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.ask_research import ask_question

app = FastAPI(
    title="ResearchLens API",
    description="Ask questions about research papers using RAG.",
    version="1.0.0",
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def home():
    return {"message": "ResearchLens API is running!"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        answer = ask_question(question)
        return AskResponse(question=question, answer=answer)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer. Check the backend logs.",
        ) from exc
