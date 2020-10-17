from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from db import crud, models, database, schemas

# Create declarative database tables (SQLAlchemy)
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/answers/", tags=["application"])
def create_answer(answer: schemas.AnswerCreate):
    return None

@app.post("/questions/", tags=["application"])
def create_question(question: schemas.QuestionCreate):
    return None

@app.get("/questions/", tags=["application"], response_model=schemas.Question)
def read_questions(q: Optional[str] = None):
    return None

@app.post("/users/", tags=["application"])
def create_user(user: schemas.UserCreate):
    return None

@app.get("/users/", tags=["application"], response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users