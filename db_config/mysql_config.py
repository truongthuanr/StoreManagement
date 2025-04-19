from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/budoland"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
