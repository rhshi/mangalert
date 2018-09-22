from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, URL, Regexp

from app.models import User
from app.src.init_follows import checkValid


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about me', validators=[Length(min=0, max=140)])
    mdlist = StringField('update mdlist (leave blank to delete list)', validators=[Length(min=0, max=48)])
    submit = SubmitField('submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('this username is not available')

    def validate_mdlist(self, mdlist):
        if len(mdlist.data) > 0:
            URL(mdlist)
        else:
            pass


class MDListForm(FlaskForm):
    mdlist = StringField('mdlist link:', validators=[DataRequired(), Length(min=1, max=48), URL()])
    submit = SubmitField('submit')

    def validate_mdlist(self, mdlist):
        if 'mangadex.org/list/' not in mdlist.data:
            raise ValidationError('this is not a valid mdlist')
        elif checkValid(mdlist.data):
            raise ValidationError('your mdlist is private. please make it public in your mangadex settings.')


class PostForm(FlaskForm):
    title = StringField('title', validators=[(DataRequired())])
    link = StringField('link (optional)', validators=[Regexp('^[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', message='Invalid URL')])
    post = TextAreaField('say something', validators=[
        DataRequired(), Length(min=1, max=480)])
    submit = SubmitField('submit')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')