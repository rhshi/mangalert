from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, URL

from app.models import User
from app.src.init_follows import checkValid


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about me', validators=[Length(min=0, max=140)])
    submit = SubmitField('submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('this username is not available')


class MDListForm(FlaskForm):
    mdlist = StringField('mdlist link:', validators=[DataRequired(), Length(min=1, max=48), URL()])
    submit = SubmitField('submit')

    def validate_mdlist(self, mdlist):
        if 'mangadex.org/list/' not in mdlist.data:
            raise ValidationError('this is not a valid mdlist')
        elif checkValid(mdlist.data):
            raise ValidationError('your mdlist is private. please make it public in your mangadex settings.')


class PostForm(FlaskForm):
    post = TextAreaField('say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    title = StringField('title', validators=[(DataRequired())])
    link = StringField('link (optional)')
    submit = SubmitField('submit')