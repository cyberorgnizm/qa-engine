from fastapi import FastAPI
from typing import Optional
from models.schemas import UserCreate, QuestionCreate, Question, AnswerCreate

app = FastAPI()


@app.post("/answers/", tags=["application"])
def create_answer(answer: AnswerCreate):
    return None

@app.post("/questions/", tags=["application"])
def create_question(question: QuestionCreate):
    return None

@app.get("/questions/", tags=["application"], response_model=Question)
def read_questions(q: Optional[str] = None):
    return None

@app.post("/users/", tags=["application"])
def create_user(user: UserCreate):
    return None
