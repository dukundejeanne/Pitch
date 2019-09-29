from flask_wtf import  FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

from ..models import Article

class UpdateBlogForm(FlaskForm):
    title=StringField('Title', validators=[Required()])
    category=SelectField('Category',choices=[('Music','Music'),('Job','Job'),('News','News')], validators=[Required()])
    post=TextAreaField('Your Post.', validators=[Required()])
    submit=SubmitField('save')

class PitchForm(FlaskForm):
    title=StringField('Title', validators=[Required()])
    category=SelectField('Category',choices=[('Music','Music'),('Job','Job'),('News','News')], validators=[Required()])
    post=TextAreaField('Your Post', validators=[Required()])
    submit=SubmitField('Pitch')

class CommentForm(FlaskForm):
    comment=TextAreaField('Leave a comment',validators=[Required()])
    submit=SubmitField('Comment')

class BlogForm(FlaskForm):

    post=TextAreaField('Title',validators=[Required()])
    category=StringField('Your Pitch.', validators=[Required()])
    submit = SubmitField('Submit')

class ArticleUploadForm(FlaskForm):
    article = TextAreaField('Article',validators=[Required()])
    category = StringField('Title',validators=[Required()])
    submit = SubmitField('Add Article')

# class CategoryForm(FlaskForm):
#     category=TextAreaField('Category')
#     submit=SubmitField()
