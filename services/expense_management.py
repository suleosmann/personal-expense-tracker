from models.expense import Expense
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class ExpenseService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_expense(self, user_id, amount, description, date):
        try:
            new_expense = Expense(user_id=user_id, amount=amount, description=description, date=date)
            self.db_session.add(new_expense)
            self.db_session.commit()
            return new_expense
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def get_expenses(self, user_id):
        try:
            return self.db_session.query(Expense).filter(Expense.user_id == user_id).all()
        except SQLAlchemyError as e:
            raise e

    def update_expense(self, expense_id, amount=None, description=None, date=None):
        try:
            expense = self.db_session.query(Expense).filter(Expense.id == expense_id).first()
            if expense:
                if amount is not None:
                    expense.amount = amount
                if description is not None:
                    expense.description = description
                if date is not None:
                    expense.date = date
                self.db_session.commit()
                return expense
            return None
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def delete_expense(self, expense_id):
        try:
            expense_to_delete = self.db_session.query(Expense).filter(Expense.id == expense_id).first()
            if expense_to_delete:
                self.db_session.delete(expense_to_delete)
                self.db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
