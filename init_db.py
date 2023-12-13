from database import engine
from models.user import Base as UserBase
from models.expense import Base as ExpenseBase
from models.income import Base as IncomeBase

def init_db():
    # Create tables
    UserBase.metadata.create_all(engine)
    ExpenseBase.metadata.create_all(engine)
    IncomeBase.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized and tables created.")
