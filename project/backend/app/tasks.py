# backend/app/tasks.py

from app.celery_app import celery_app
from app.database import SessionLocal
from app.rag.retriever import retrieve
from app.rag.generator import (
    build_context_from_retrieved,
    generate_rag_answer_local
)
from app.rag.model import QueryLog
import time


@celery_app.task
def process_question(question: str):
    start = time.time()


    retrieved = retrieve(question, top_k=5)


    chunks_map = {r["chunk_id"]: r["text"] for r in retrieved}


    context = build_context_from_retrieved(
        retrieved_list=retrieved,
        chunks_map=chunks_map,
        top_k=5,
        max_chars=8000
    )


    answer = generate_rag_answer_local(
        query=question,
        context=context,
        max_new_tokens=180,
        temperature=0.0
    )


    db = SessionLocal()
    log = QueryLog(
        question=question,
        answer=answer,
        generation_time=time.time() - start
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return {"log_id": log.id}
