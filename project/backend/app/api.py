# backend/app/api.py

from fastapi import FastAPI
from app.database import SessionLocal
from app.rag.model import QueryLog
from app.tasks import process_question

from app.rag import retriever


app = FastAPI()

@app.post("/ask")
def ask(question: str):
    task = process_question.delay(question)
    return {"task_id": task.id}

@app.get("/result/{log_id}")
def get_result(log_id: int):
    db = SessionLocal()
    return db.query(QueryLog).filter(QueryLog.id == log_id).first()


@app.get("/test_retriever")
def rag_test(query: str, top_k: int = 5):
    results = retriever.retrieve(query, top_k=top_k)
    return {"results": results}
