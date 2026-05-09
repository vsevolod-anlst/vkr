# backend/app/api.py

from fastapi import FastAPI
from app.database import SessionLocal
from app.rag.model import QueryLog



app = FastAPI()

@app.post("/ask")
def ask(question: str):
    from app.tasks import process_question
    task = process_question.delay(question)
    return {"task_id": task.id}

@app.get("/result/{log_id}")
def get_result(log_id: int):
    db = SessionLocal()
    row = db.query(QueryLog).filter(QueryLog.id == log_id).first()
    if not row:
        return {"status": "not_ready"}
    return {
        "id": row.id,
        "question": row.question,
        "answer": row.answer,
        "generation_time": row.generation_time,
        "created_at": row.created_at
    }
