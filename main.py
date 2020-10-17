from fastapi import FastAPI, Depends, HTTPException, status
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


@app.post("/answers/", tags=["application"], deprecated=True)
def create_answer(answer: schemas.AnswerCreate):
    return None

# ========================
# Questions endpoints
# ========================

@app.post("/users/{user_id}/questions/", tags=["application"], response_model=schemas.Question)
def create_question_for_user(user_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question, user_id=user_id)

@app.get("/users/{user_id}/questions/", tags=["application"], response_model=List[schemas.Question])
def read_questions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: return question only for user_id
    db_questions = crud.get_questions(db=db, skip=skip, limit=limit)
    return db_questions

# ========================
# User endpoints
# ========================

@app.post("/users/", tags=["application"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", tags=["application"], response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}/", tags=["application"], response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
