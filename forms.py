from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField


class NewPost(FlaskForm):
    title = StringField('Blog Title')
    subtitle = StringField('Subtitle')
    author = StringField('Author')
    img_url = StringField('Background Image URL')
    body = CKEditorField('Body')
    submit = SubmitField("Add Post")