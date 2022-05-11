from datetime import datetime

from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import db
from flask_login import UserMixin


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, unique=False)
    type = db.Column(db.String(80), nullable=False, unique=False)

    user = relationship("User", secondary="transaction_user")

    def __init__(self, amount, type):
        self.amount = float(amount)
        self.type = type


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False, unique=True)
    about = db.Column(db.String(300), nullable=True, unique=False)
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on', db.DateTime)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    is_admin = db.Column('is_admin', db.Boolean(), nullable=False, server_default='0')

    # `roles` and `groups` are reserved words that *must* be defined
    # on the `User` model to use group- or role-based authorization.

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.email


class Transaction_user(db.Model):
    __tablename__ = 'transaction_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    user = relationship(User, backref=backref("transaction_user", cascade="all, delete-orphan"))
    transaction = relationship(Transaction, backref=backref("transaction_user", cascade="all, delete-orphan"))
