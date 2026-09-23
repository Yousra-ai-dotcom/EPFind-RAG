"""
Modèles SQLAlchemy — tables PostgreSQL
Responsable : Personne 2 (complété ici pour débloquer la démo)

Chaque classe = une table. Chaque attribut = une colonne.
"""

from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Float
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    microsoft_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="user")
    quizzes = relationship("Quiz", back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Nouvelle conversation")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.created_at"
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # "user" ou "assistant"
    content = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)  # JSON stocké en texte
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course = Column(String, nullable=False)
    level = Column(String, default="facile")
    questions_json = Column(Text, nullable=False)  # les questions générées, en JSON
    score = Column(Float, nullable=True)
    number_questions = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quizzes")
