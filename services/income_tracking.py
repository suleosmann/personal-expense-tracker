from models.income import Income
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class IncomeService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_income(self, user_id, amount, source, date):
        try:
            new_income = Income(user_id=user_id, amount=amount, source=source, date=date)
            self.db_session.add(new_income)
            self.db_session.commit()
            return new_income
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def get_incomes(self, user_id):
        try:
            return self.db_session.query(Income).filter(Income.user_id == user_id).all()
        except SQLAlchemyError as e:
            raise e

    def update_income(self, income_id, amount=None, source=None, date=None):
        try:
            income = self.db_session.query(Income).filter(Income.id == income_id).first()
            if income:
                if amount is not None:
                    income.amount = amount
                if source is not None:
                    income.source = source
                if date is not None:
                    income.date = date
                self.db_session.commit()
                return income
            return None
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def delete_income(self, income_id):
        try:
            income_to_delete = self.db_session.query(Income).filter(Income.id == income_id).first()
            if income_to_delete:
                self.db_session.delete(income_to_delete)
                self.db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
