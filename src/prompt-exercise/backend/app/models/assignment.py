from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
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
    
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    response_prompt = Column(String, nullable=False)
    response_llm_answer = Column(String, nullable=False)
    response_ai_provider = Column(String, nullable=False)
    response_ai_model = Column(String, nullable=False)
    response_ai_input_tokens = Column(Integer, nullable=False)
    response_ai_output_tokens = Column(Integer, nullable=False)
    response_ai_seconds = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    select_for_submission = Column(Boolean, default=False)
    submission_time = Column(DateTime(timezone=True))
    # user = relationship("User", back_populates="user_responses")

