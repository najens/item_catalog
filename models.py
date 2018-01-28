from  flask import current_app
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

# Define User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    provider = db.Column(db.String(32), server_default='')
    created_at = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(32), server_default='')
    email = db.Column(db.String(32), index=True, unique=True, nullable=False)
    picture = db.Column(db.String(150), server_default='')
    roles = db.relationship('Role', cascade='all,delete', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    categories = db.relationship('Category', cascade='all,delete',
            backref=db.backref('user', lazy=True))
    items = db.relationship('Item', cascade='all,delete',
            backref=db.backref('user', lazy=True))

    def generate_public_id(self):
        self.public_id = str(uuid.uuid4())

    def generate_created_at(self):
        self.created_at = str(datetime.utcnow())

# Define Role model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    label = db.Column(db.Unicode(255),)

# Define UserRoles model
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.public_id',
            ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id',
            ondelete='CASCADE'))

# Define Category model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.public_id'),
            nullable=False)
    items = db.relationship('Item', cascade='all,delete', backref='category', lazy=True)

# Define Item model
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.public_id'))
    category_name = db.Column(db.String(), db.ForeignKey('category.name'))
