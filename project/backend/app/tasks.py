# backend/app/tasks.py

from app.database import SessionLocal
from app.models import QueryLog
from app.celery_app import celery_app

@celery_app.task
def process_question(question: str):
    # здесь ты делаешь RAG
    start = time.monotonic()
    # вызываешь модель / RAG
    end = time.monotonic()
    generation_time = end - start
    # ---------------------------------------------------------------------
    db = SessionLocal()
    log = QueryLog(
        question=question,
        answer=answer,
        generation_time=generation_time
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return log.id
