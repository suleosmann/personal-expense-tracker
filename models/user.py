from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Relationships
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
