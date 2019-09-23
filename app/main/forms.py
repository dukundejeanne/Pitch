from flask_wtf import  FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio=TextAreaField('write a brief bio about you.', validators=[Required()])
    submit=SubmitField('save')

class PitchForm(FlaskForm):
    title=StringField('Title', validators=[Required()])
    category=SelectField('Category',choices=[('Music','Music'),('Job','Job'),('News','News')], validators=[Required()])
    post=TextAreaField('Your Pitch.', validators=[Required()])
    submit=SubmitField('Pitch')

class CommentForm(FlaskForm):
    comment=TextAreaField('Leave a comment',validators=[Required()])
    submit=SubmitField('Comment')

class CategoryForm(FlaskForm):

    title = StringField('Title',validators=[Required()])
    post=TextAreaField('Your Pitch.', validators=[Required()])
    submit = SubmitField('Submit')
    

# class CategoryForm(FlaskForm):
#     category=TextAreaField('Category')
#     submit=SubmitField()
