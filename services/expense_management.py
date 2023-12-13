from models.expense import Expense
from sqlalchemy.orm import Session

class ExpenseService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_expense(self, user_id, amount, description, date):
        new_expense = Expense(user_id=user_id, amount=amount, description=description, date=date)
        self.db_session.add(new_expense)
        self.db_session.commit()
        return new_expense

    def get_expenses(self, user_id):
        return self.db_session.query(Expense).filter(Expense.user_id == user_id).all()

    # Implement update and delete methods for expenses as needed
