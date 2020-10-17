from sqlalchemy.orm import Session
from .models import Question, Answer, User
from .schemas import UserCreate, QuestionCreate


def get_user(db: Session, user_id: int):
    """An ORM query to a user by filtering user by `user_id`"""
    query = db.query(User).filter(User.id == user_id).first()
    return query


def get_user_by_email(db: Session, email: str):
    """An ORM query to a user by filtering user by `email`"""
    query = db.query(User).filter(User.email == email).first()
    return query


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """An ORM query to get all users"""
    query = db.query(User).offset(skip).limit(limit).all()
    return query


def create_user(db: Session, user: UserCreate):
    """An ORM query to create a new `User`"""
    # hash password
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        email=user.email,
        hashed_password=fake_hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    """An ORM query to get all questions"""
    query = db.query(Question).offset(skip).limit(limit).all()
    return query

def create_question(db: Session, question: QuestionCreate, user_id: int):
    """An ORM query to create a new `Question`"""
    print(question)
    db_question = Question(**question.dict(), owner_id=user_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
