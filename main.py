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
        expense_service = ExpenseService(session)
        income_service = IncomeService(session)

        username = click.prompt("Enter Username")
        password = click.prompt("Enter Password", hide_input=True)

        user = auth_service.login_user(username, password)
        if user:
            click.echo(f"User {user.username} logged in successfully.")

            # Display user information
            user_info = [["Username", user.username], ["Email", user.email]]
            click.echo(tabulate(user_info, headers=["Field", "Value"], tablefmt="grid"))

            # Fetch and display expenses
            expenses = expense_service.get_expenses(user.id)
            if expenses:
                expense_data = [[exp.date, exp.description, f"${exp.amount}"] for exp in expenses]
                click.echo("\nExpenses:")
                click.echo(tabulate(expense_data, headers=["Date", "Description", "Amount"], tablefmt="grid"))
            else:
                click.echo("\nNo expenses recorded.")

            # Fetch and display incomes
            incomes = income_service.get_incomes(user.id)
            if incomes:
                income_data = [[inc.date, inc.source, f"${inc.amount}"] for inc in incomes]
                click.echo("\nIncomes:")
                click.echo(tabulate(income_data, headers=["Date", "Source", "Amount"], tablefmt="grid"))
            else:
                click.echo("\nNo incomes recorded.")
        else:
            click.echo("Invalid username or password.")

@cli.command(help="Add a new expense")
def add_expense():
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        user_id = click.prompt("Enter User ID", type=int)
        amount = click.prompt("Enter Amount", type=float)
        description = click.prompt("Enter Description")
        date = click.prompt("Enter Date (YYYY-MM-DD)", type=str)

        try:
            expense = expense_service.add_expense(user_id, amount, description, date)
            click.echo(f"Added expense: {expense.description} of amount {expense.amount} on {expense.date}")
        except SQLAlchemyError as e:
            click.echo(f"Error adding expense: {e}")

@cli.command(help="List all expenses for a user")
@click.argument('user_id', type=int)
def list_expenses(user_id):
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        try:
            expenses = expense_service.get_expenses(user_id)
            table = [[expense.date, expense.description, f"${expense.amount}"] for expense in expenses]
            click.echo(tabulate(table, headers=["Date", "Description", "Amount"], tablefmt="grid"))
        except SQLAlchemyError as e:
            click.echo(f"Error retrieving expenses: {e}")

@cli.command(help="Add a new income")
def add_income():
    with SessionFactory() as session:
        income_service = IncomeService(session)
        user_id = click.prompt("Enter User ID", type=int)
        amount = click.prompt("Enter Amount", type=float)
        source = click.prompt("Enter Source")
        date = click.prompt("Enter Date (YYYY-MM-DD)", type=str)

        try:
            income = income_service.add_income(user_id, amount, source, date)
            click.echo(f"Added income: {income.source} of amount {income.amount} on {income.date}")
        except SQLAlchemyError as e:
            click.echo(f"Error adding income: {e}")

@cli.command(help="List all incomes for a user")
@click.argument('user_id', type=int)
def list_incomes(user_id):
    with SessionFactory() as session:
        income_service = IncomeService(session)
        try:
            incomes = income_service.get_incomes(user_id)
            table = [[income.date, income.source, f"${income.amount}"] for income in incomes]
            click.echo(tabulate(table, headers=["Date", "Source", "Amount"], tablefmt="grid"))
        except SQLAlchemyError as e:
            click.echo(f"Error retrieving incomes: {e}")
@cli.command(help="Delete a user")
@click.argument('user_id', type=int)
def delete_user(user_id):
    with SessionFactory() as session:
        auth_service = AuthService(session)
        if auth_service.delete_user(user_id):
            click.echo(f"User with ID {user_id} deleted successfully.")
        else:
            click.echo("User not found or unable to delete.")

@cli.command(help="Delete an expense")
@click.argument('expense_id', type=int)
def delete_expense(expense_id):
    with SessionFactory() as session:
        expense_service = ExpenseService(session)
        if expense_service.delete_expense(expense_id):
            click.echo(f"Expense with ID {expense_id} deleted successfully.")
        else:
            click.echo("Expense not found or unable to delete.")

@cli.command(help="Delete an income")
@click.argument('income_id', type=int)
def delete_income(income_id):
    with SessionFactory() as session:
        income_service = IncomeService(session)
        if income_service.delete_income(income_id):
            click.echo(f"Income with ID {income_id} deleted successfully.")
        else:
            click.echo("Income not found or unable to delete.")
@cli.command(help="List all users")
def list_users():
    with SessionFactory() as session:
        auth_service = AuthService(session)
        users = auth_service.get_all_users()

        # Prepare data for tabulation
        user_data = [[user.id, user.username, user.email] for user in users]
        headers = ["ID", "Username", "Email"]

        # Display the table
        click.echo(tabulate(user_data, headers, tablefmt="grid"))

if __name__ == '__main__':
    cli()
