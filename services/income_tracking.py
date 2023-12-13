from models.income import Income
from sqlalchemy.orm import Session

class IncomeService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_income(self, user_id, amount, source, date):
        new_income = Income(user_id=user_id, amount=amount, source=source, date=date)
        self.db_session.add(new_income)
        self.db_session.commit()
        return new_income

    def get_incomes(self, user_id):
        return self.db_session.query(Income).filter(Income.user_id == user_id).all()

    # Implement update and delete methods for incomes as needed
