from fastapi import FastAPI
from pydantic import BaseModel
from app.database import SessionLocal
from app.rag.model import QueryLog
from app.tasks import process_question



app = FastAPI()

class AskRequest(BaseModel):
    question: str
    chat_id: int
    user_id: int
    message_id: int

@app.post("/ask")
def ask(req: AskRequest):
    task = process_question.delay(req.question, req.chat_id, req.user_id, req.message_id)
    return {"task_id": task.id}

@app.get("/history/{user_id}")
def get_history(user_id: int):
    db = SessionLocal()
    rows = (
        db.query(QueryLog)
        .filter(QueryLog.user_id == user_id)
        .order_by(QueryLog.created_at.desc())
        .all()
    )
    return [
        {
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "created_at": r.created_at
        } 
        for r in rows
    ]

@app.get("/health")
def health():
    return {"status": "ok"}

