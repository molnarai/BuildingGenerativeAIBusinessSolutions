from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

from .auth import User


class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    number_of_required_responses = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    ai_input_tokens = Column(Integer, nullable=True)
    ai_max_tokens = Column(Integer, nullable=True)
    ai_model = Column(String, nullable=True)
    ai_output_tokens = Column(Integer, nullable=True)
    ai_provider = Column(String, nullable=True)
    ai_seconds = Column(Float, nullable=True)
    ai_stream = Column(Boolean, nullable=True)
    ai_temperature = Column(Float, nullable=True)
    ai_timestamp = Column(String, nullable=True)
    llm_answer = Column(String, nullable=True)
    problem_description = Column(String, nullable=True)
    problem_id = Column(Integer, nullable=True)
    problem_title = Column(String, nullable=True)
    prompt = Column(String, nullable=True)
    select_for_submission = Column(Boolean, nullable=True)
    user_comment = Column(String, nullable=True)
    username = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    # user = relationship("User", back_populates="user_responses")

