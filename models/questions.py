from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Question(Base):
    """
    SQLAlchemy model for questions
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(250), unique=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
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
    owner_id = Column(Integer, ForeignKey("user.id"))
    question_id = Column(Integer, ForeignKey("question.id"))

    owner = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
