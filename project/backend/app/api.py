# backend/app/api.py

from fastapi import FastAPI
from app.database import SessionLocal
from app.rag.model import QueryLog
from app.tasks import process_question

app = FastAPI()

@app.post("/ask")
def ask(question: str):
    task = process_question.delay(question)
    return {"task_id": task.id}

@app.get("/result/{log_id}")
def get_result(log_id: int):
    db = SessionLocal()
    return db.query(QueryLog).filter(QueryLog.id == log_id).first()
