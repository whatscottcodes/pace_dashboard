from sqlalchemy import Table
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from .settings import user_db

engine = create_engine(f"sqlite:///{user_db}")

db = SQLAlchemy()


class User(db.Model):
    """
    Class for logging in and logging out users
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


User_tbl = Table("user", User.metadata)


def add_user(username, password, email):
    """
    Adds a user to the table with a hashed password

    Args:
        username(str): username of user
        password(str): non-hashed password string
        email(str): email of user
    """
    hashed_password = generate_password_hash(password, method="sha256")

    ins = User_tbl.insert().values(
        username=username, email=email, password=hashed_password
    )

    conn = engine.connect()
    conn.execute(ins)
    conn.close()
