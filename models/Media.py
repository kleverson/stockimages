from sqlalchemy import ForeignKey, event
from app import db


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text)

    media_id = db.Column(db.Integer(), ForeignKey('media.id'))
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class Color(db.Model):
    __tablename__ = "color"

    id = db.Column(db.Integer(), primary_key=True)
    color = db.Column(db.Text)
    media_id = db.Column(db.Integer(), ForeignKey('media.id'))
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class Download(db.Model):
    __tablename__ = "download"

    id = db.Column(db.Integer(), primary_key=True)
    media_id = db.Column(db.Integer(), ForeignKey('media.id'))
    user_id = db.Column(db.Integer(), ForeignKey("users.id"))

    download_date = db.Column(db.DateTime())

class Interaction(db.Model):
    __tablename__ = "interaction"

    id = db.Column(db.Integer(), primary_key=True)

    media_id = db.Column(db.Integer(), ForeignKey('media.id'))
    user_id = db.Column(db.Integer(), ForeignKey('users.id'))

    type = db.Column(db.String(2))
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey("users.id"))
    media_id = db.Column(db.Integer(), ForeignKey('media.id'))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text)
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())

class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text)
    file = db.Column(db.Text)
    resolution = db.Column(db.String(25))
    vertical = db.Column(db.Boolean)
    dominant_color = db.Column(db.String(7))
    file_type = db.Column(db.String(20))
    is_public = db.Column(db.Boolean(), default=False)

    interaction = db.relationship("Interaction")

    user_id = db.Column(db.Integer(), ForeignKey('users.id'))

    category_id = db.Column(db.Integer(), ForeignKey("category.id"))
    category = db.relationship("Category")

    tags = db.relationship("Tag")
    colors = db.relationship("Color")

    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())