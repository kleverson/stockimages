from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import SelectMultipleField, StringField, FileField, BooleanField, validators, SelectField

from models.Media import Category

class FormMediaAdd(FlaskForm):

    name = StringField("name", [validators.Length(min=4, max=255), validators.DataRequired()])
    file = FileField("file")
    vertical = BooleanField("vertical")
    tag = StringField('tag')
    category =  SelectField('category', choices=[(c.id, c.name) for c in Category.query.order_by(Category.name.asc()).all()], coerce=int)

class FormSearchMedia(FlaskForm):
    name = StringField('term')
    category = SelectField('category',choices=[(c.id, c.name) for c in Category.query.order_by(Category.name.asc()).all()], coerce=int, default=21)
    vertical = BooleanField("vertical")

