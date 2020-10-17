import toml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# load TOML app config file as `dict`
config = toml.load("./configs/app.toml")

engine = create_engine(
    config['database']["DATABASE_URL"],
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine.connect()

Base = declarative_base()