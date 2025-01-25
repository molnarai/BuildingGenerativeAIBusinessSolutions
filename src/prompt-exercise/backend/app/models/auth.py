from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    tokens = relationship("AuthToken", back_populates="user")
    client_data = relationship("ClientData", back_populates="user")

class AuthToken(Base):
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True, nullable=False)
    refresh_token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="tokens")

class ClientData(Base):
    __tablename__ = "client_data"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_agent = Column(String)
    ip_address = Column(String)
    last_login = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="client_data")
