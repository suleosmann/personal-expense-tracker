from models.user import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def register_user(self, username, email, password):
        try:
            password_hash = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=password_hash)
            self.db_session.add(new_user)
            self.db_session.commit()
            return new_user
        except IntegrityError:
            self.db_session.rollback()
            # Here you can decide how to handle the error. 
            # You might want to raise a custom exception or return a specific message.
            raise ValueError("A user with the given username or email already exists.")

    def login_user(self, username, password):
        user = self.db_session.query(User).filter(User.username == username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def get_all_users(self):
        return self.db_session.query(User).all()
