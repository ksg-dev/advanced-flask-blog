from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField


class NewPost(FlaskForm):
    title = StringField('Title')
    subtitle = StringField('Subtitle')
    body = CKEditorField('Body')
    author = StringField('Author')
    img_url = StringField('Background Image URL')
    submit = SubmitField("Add Post")