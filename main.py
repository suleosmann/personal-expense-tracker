import click
from sqlalchemy.exc import SQLAlchemyError
from database import SessionFactory
from services.auth import AuthService
from services.expense_management import ExpenseService
from services.income_tracking import IncomeService
from tabulate import tabulate

# Command-line interface setup using Click
@click.group()
def cli():
    """Expense Tracker CLI Application"""
    pass

@cli.command(help="Register a new user")
@click.argument('username')
@click.argument('email')
@click.argument('password')
def register(username, email, password):
    with SessionFactory() as session:
        auth_service = AuthService(session)
        try:
            user = auth_service.register_user(username, email, password)
            click.echo(f"User {user.username} registered successfully.")
        except SQLAlchemyError as e:
            click.echo(f"Error registering user: {e}")

@cli.command(help="Login a user")
@click.argument('username')
@click.argument('password')
def login(username, password):
    with SessionFactory() as session:
        auth_service = AuthService(session)
        user = auth_service.login_user(username, password)
        if user:
            click.echo(f"User {user.username} logged in successfully.")
        else:
            click.echo("Invalid username or password.")

@cli.command(help="Add a new expense")
@click.argument('user_id', type=int)
@click.argument('amount', type=float)
@click.argument('description')
@click.argument('date', type=click.DateTime(formats=["%Y-%m-%d"]))
def add_expense(user_id, amount, description, date):
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        expense = expense_service.add_expense(user_id, amount, description, date)
        click.echo(f"Added expense: {expense.description} of amount {expense.amount} on {expense.date}")

@cli.command(help="List all expenses for a user")
@click.argument('user_id', type=int)
def list_expenses(user_id):
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        expenses = expense_service.get_expenses(user_id)
        # Format and display the expenses in a table
        table = [[expense.date, expense.description, f"${expense.amount}"] for expense in expenses]
        click.echo(tabulate(table, headers=["Date", "Description", "Amount"], tablefmt="grid"))

@cli.command(help="Add a new income")
@click.argument('user_id', type=int)
@click.argument('amount', type=float)
@click.argument('source')
@click.argument('date', type=click.DateTime(formats=["%Y-%m-%d"]))
def add_income(user_id, amount, source, date):
    with SessionFactory() as session:
        income_service = IncomeService(session)
        income = income_service.add_income(user_id, amount, source, date)
        click.echo(f"Added income: {income.source} of amount {income.amount} on {income.date}")

@cli.command(help="List all incomes for a user")
@click.argument('user_id', type=int)
def list_incomes(user_id):
    with SessionFactory() as session:
        income_service = IncomeService(session)
        incomes = income_service.get_incomes(user_id)
        # Format and display the incomes in a table
        table = [[income.date, income.source, f"${income.amount}"] for income in incomes]
        click.echo(tabulate(table, headers=["Date", "Source", "Amount"], tablefmt="grid"))

if __name__ == '__main__':
    cli()
