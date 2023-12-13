from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///expense_tracker.db"

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
