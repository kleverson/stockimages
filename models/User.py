import binascii
import os

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_security import RoleMixin
from sqlalchemy import ForeignKey
from app import db

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), ForeignKey('users.id'))
    role_id = db.Column('role_id', db.Integer(), ForeignKey('roles.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name =db.Column(db.Text)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    active = db.Column(db.Boolean(),default=False)
    token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

    interaction = db.relationship("Interaction")
    media = db.relationship("Media")

    roles = db.relationship('Role', secondary='roles_users',backref=db.backref('users', lazy='dynamic'))



    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_token(self,token):
        self.token = binascii.b2a_hex(os.urandom(15)).decode("utf-8")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)