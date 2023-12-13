from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    source = Column(String)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="incomes")

    def __repr__(self):
        return f"<Income(amount={self.amount}, source='{self.source}', date={self.date})>"
