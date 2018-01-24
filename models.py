from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Define User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary='user_roles', # Relationships
            backref=db.backref('users', lazy='dynamic'))

# Define Role model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes
