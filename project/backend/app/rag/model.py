from sqlalchemy import Column, Integer, Text, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    generation_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat_id = Column(Integer)
    user_id = Column(Integer)
