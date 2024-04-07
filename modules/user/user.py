from database import sqlalchemy_db


class User(sqlalchemy_db.Model):
    _id = sqlalchemy_db.Column(
        sqlalchemy_db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = sqlalchemy_db.Column(sqlalchemy_db.String(100), unique=True)
    password = sqlalchemy_db.Column(sqlalchemy_db.String(100))
    first_name = sqlalchemy_db.Column(sqlalchemy_db.String(100))
    last_name = sqlalchemy_db.Column(sqlalchemy_db.String(100))
    company = sqlalchemy_db.Column(sqlalchemy_db.String(100))
