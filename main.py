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
def register():
    with SessionFactory() as session:
        auth_service = AuthService(session)

        username = click.prompt("Enter Username")
        email = click.prompt("Enter Email")
        password = click.prompt("Enter Password", hide_input=True, confirmation_prompt=True)

        try:
            user = auth_service.register_user(username, email, password)
            click.echo(f"User {user.username} registered successfully.")
        except SQLAlchemyError as e:
            click.echo(f"Error registering user: {e}")

@cli.command(help="Login a user")
def login():
    with SessionFactory() as session:
        auth_service = AuthService(session)

        username = click.prompt("Enter Username")
        password = click.prompt("Enter Password", hide_input=True)

        user = auth_service.login_user(username, password)
        if user:
            click.echo(f"User {user.username} logged in successfully.")
        else:
            click.echo("Invalid username or password.")

@cli.command(help="List all users")
def list_users():
    with SessionFactory() as session:
        auth_service = AuthService(session)
        users = auth_service.get_all_users()

        table = [[user.id, user.username, user.email] for user in users]
        click.echo(tabulate(table, headers=["ID", "Username", "Email"], tablefmt="grid"))

@cli.command(help="Add a new expense")
def add_expense():
    with SessionFactory() as session:
        expense_service = ExpenseService(session)

        user_id = click.prompt("Enter User ID", type=int)
        amount = click.prompt("Enter Amount", type=float)
        description = click.prompt("Enter Description")
        date = click.prompt("Enter Date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))

        expense = expense_service.add_expense(user_id, amount, description, date)
        click.echo(f"Added expense: {expense.description} of amount {expense.amount} on {expense.date}")

@cli.command(help="List all expenses for a user")
@click.argument('user_id', type=int)
def list_expenses(user_id):
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        expenses = expense_service.get_expenses(user_id)
        table = [[expense.date, expense.description, f"${expense.amount}"] for expense in expenses]
        click.echo(tabulate(table, headers=["Date", "Description", "Amount"], tablefmt="grid"))

@cli.command(help="Add a new income")
def add_income():
    with SessionFactory() as session:
        income_service = IncomeService(session)

        user_id = click.prompt("Enter User ID", type=int)
        amount = click.prompt("Enter Amount", type=float)
        source = click.prompt("Enter Source")
        date = click.prompt("Enter Date (YYYY-MM-DD)", type=click.DateTime(formats=["%Y-%m-%d"]))

        income = income_service.add_income(user_id, amount, source, date)
        click.echo(f"Added income: {income.source} of amount {income.amount} on {income.date}")

@cli.command(help="List all incomes for a user")
@click.argument('user_id', type=int)
def list_incomes(user_id):
    with SessionFactory() as session:
        income_service = IncomeService(session)
        incomes = income_service.get_incomes(user_id)
        table = [[income.date, income.source, f"${income.amount}"] for income in incomes]
        click.echo(tabulate(table, headers=["Date", "Source", "Amount"], tablefmt="grid"))

if __name__ == '__main__':
    cli()
