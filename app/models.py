from app import db, ma
import uuid
from flask_login import UserMixin
from flask_security import RoleMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


# Define User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(32), server_default='')
    email = db.Column(db.String(32), index=True, unique=True, nullable=False)
    picture = db.Column(db.String(150), server_default='')
    roles = db.relationship(
        'Role',
        cascade='all,delete',
        secondary='user_roles',
        backref=db.backref('users', lazy='dynamic')
    )
    categories = db.relationship(
        'Category',
        cascade='all,delete',
        backref=db.backref('user', lazy=True)
    )
    items = db.relationship(
        'Item',
        cascade='all,delete',
        backref=db.backref('user', lazy=True)
    )

    def generate_public_id(self):
        """Generates random public id"""
        self.public_id = str(uuid.uuid4())


# Define Role model
class Role(RoleMixin, db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    label = db.Column(db.Unicode(255),)


# Define UserRoles model
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.public_id', ondelete='CASCADE')
    )
    role_id = db.Column(
        db.Integer(),
        db.ForeignKey('role.id', ondelete='CASCADE')
    )


# Define OAuth model
class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.public_id'))
    user = db.relationship('User')


# Define Category model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.public_id'),
        nullable=False
    )
    items = db.relationship(
        'Item',
        cascade='all,delete',
        backref='category',
        lazy=True
    )


# Define Item model
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.public_id'))
    category_name = db.Column(db.String(), db.ForeignKey('category.name'))


# Define UserSchema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        ordered = True
        exclude = ('id', 'password_hash')

    roles = fields.Nested('RoleSchema', many=True, load=True)
    categories = fields.Nested('CategorySchema', many=True, load=True)


# Define RoleSchema
class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role


# Define UserRolesSchema
class UserRolesSchema(ma.ModelSchema):
    class Meta:
        model = UserRoles


# Define Category Schema
class CategorySchema(ma.ModelSchema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'user_id', 'link', 'items')

    link = ma.URLFor('api.get_one_category', id='<id>')
    items = fields.Nested('ItemSchema', many=True, load=True)


# Define ItemSchema
class ItemSchema(ma.ModelSchema):
    class Meta:
        ordered = True
        # Fields to expose
        fields = (
            'id', 'name', 'description', 'user_id', 'category_name', 'link'
        )

    # Smart hyperlinking
    link = ma.URLFor('api.get_one_item', id='<id>')
