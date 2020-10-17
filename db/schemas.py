from typing import List, Optional
from pydantic import BaseModel

class QuestionBase(BaseModel):
    text: str
    answer: str

class Question(QuestionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class QuestionCreate(QuestionBase):
    pass


class AnswerBase(BaseModel):
    text: str
    owner: int
    question_id: int

class Answer(AnswerBase):
    id: int
    is_correct: bool

    class Config:
        orm_mode = True

class AnswerCreate(AnswerBase):
    pass


class Contribution(BaseModel):
    questions: List[Question] = []
    answers: List[Answer] = []


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # contribution: Optional[Contribution]
    questions: Optional[List[Question]]

    class Config:
        orm_mode = True