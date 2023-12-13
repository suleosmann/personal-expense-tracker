# Expense Tracker Application

## Overview
This Expense Tracker is a Python-based command-line application designed for personal finance management. It allows users to efficiently track their expenses and incomes.

## Features
- User Registration and Authentication
- Add, View, Update, and Delete Expenses
- Add, View, Update, and Delete Incomes
- Data stored in SQLite database

## Prerequisites
- Python 3.x
- SQLAlchemy
- Werkzeug
- Click

## Installation

### Clone the repository and navigate to the project directory:
git clone [URL of your repository]
cd expense_tracker


### Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate # Unix or MacOS
venv\Scripts\activate # Windows


### Install dependencies:
pip install -r requirements.txt


## Database Initialization

Before running the application, initialize the database:
python init_db.py


## Usage

Run the application using:
python main.py --help


This command displays all available commands.

### Example Commands
- **Register a User**: 
python main.py register [username] [email] [password]

- **Login a User**: 
python main.py login [username] [password]

- **Add an Expense**: 
python main.py add_expense [user_id] [amount] [description] [date]

- **List Expenses**: 
python main.py list_expenses [user_id]


(Add similar instructions for managing incomes.)

## Project Structure
- `/models` - Contains SQLAlchemy ORM classes.
- `/services` - Business logic for user authentication, expense, and income management.
- `/utils` - Utility functions, including input validation.
- `main.py` - Entry point for the CLI application.

## Contributing
We welcome contributions to the Expense Tracker project. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

## License
[Your chosen license]

