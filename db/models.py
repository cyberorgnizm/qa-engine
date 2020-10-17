from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    questions = relationship("Question", back_populates="owner")
    answers = relationship("Answer", back_populates="owner")


class Question(Base):
    """
    SQLAlchemy model for questions
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    answer = Column(String(250))

    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    """
    SQLAlchemy model for answers
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), unique=True)
    is_correct = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    owner = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
