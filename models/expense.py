from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(amount={self.amount}, description='{self.description}', date={self.date})>"
