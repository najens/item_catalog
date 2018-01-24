from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Define User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(32), server_default='')
    email = db.Column(db.String(32), index=True, unique=True, nullable=False)
    picture = db.Column(db.String(150), server_default='')
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    categories = db.relationship('Category',
            backref=db.backref('user', lazy=True))
    items = db.relationship('Item', backref=db.backref('user', lazy=True))

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
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id',
            ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id',
            ondelete='CASCADE'))

# Define Category model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    user_id = db.Columng(db.Integer(), db.ForeignKey('user.id'),
            nullable=False)
    items = db.relationship('Item', backref='category', lazy=True)

# Define Item model
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id',
            ondelete='CASCADE'))
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id',
            ondelete='CASCADE'))
