from flask import render_template,url_for,abort,redirect,request
from . import main
from flask_login import login_user,login_required,current_user
# from .forms import RegistrationForm,LoginForm
from ..models import User,Pitch,Comment,Quotes,Article
from .. import db,photos
from .forms import UpdateBlogForm,PitchForm,CommentForm,BlogForm
import requests

from ..requests import getQuotes

@main.route('/')
def index():
    pitches=Pitch.query.all()
    job=Pitch.query.filter_by(category='Job').all()
    music=Pitch.query.filter_by(category='Music').all()
    news=Pitch.query.filter_by(category='News').all()
    articles = Article.get_article()
    try:
        quotes = getQuotes()
    except Exception as e:
        quotes = "quotes unavailable"
    # title='Welcome to the article'
    # return render_template('index.html',quotes = quotes)
    # category=Category.get_categories()
    # return render_template('index.html',category=category)

    return render_template('index.html',job=job,music=music,pitches=pitches,news=news,quotes = quotes)



@main.route('/create_new',methods=['GET','POST'])
@login_required
def new_pitch():
    form=PitchForm()
    if form.validate_on_submit():
        title=form.title.data
        post=form.post.data
        category=form.category.data
        user_id=current_user
        new_pitch_object=Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch_object.save_p()
        return redirect(url_for('main.index'))
    return render_template('create.html',form=form)


@main.route('/comment/<int:pitch_id>',methods=['GET','POST'])
@login_required
def comment(pitch_id):
    form=CommentForm()
    pitch=Pitch.query.get(pitch_id)
    all_comments=Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        comment=form.comment.data
        pitch_id=pitch_id
        user_id=current_user._get_current_object().id
        new_comment=Comment(comment=comment,pitch_id=pitch_id)
        new_comment.save_c() 
        return redirect(url_for('.comment',pitch_id=pitch_id))
    return render_template('comment.html',form=form,pitch=pitch,all_comments=all_comments)


@main.route('/index/<int:pitch_id>/delete',methods=['GET','POST'])
@login_required
def delete(pitch_id):
    current_post= Pitch.query.filter_by(id = pitch_id).first()
    if current_post.user != current_user:
        abort(403)
    db.session.delete(current_post)
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/index/<int:id>/delet',methods=['GET','POST'])
@login_required
def delet(id):

    comment= Comment.query.filter_by(id = id).first()

    if comment is None:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.index'))
    # return render_template('comment.html',current_post=current_post)

  

@main.route('/profile/<int:pitch_id>/',methods=['GET','POST'])
@login_required
def update_blog(pitch_id):



    current_post= Pitch.query.filter_by(id = pitch_id).first()
   

    if current_post.user != current_user:
        abort(403)
    form=UpdateBlogForm()
    if form.validate_on_submit():
        current_post.title=form.title.data
        current_post.category=form.category.data
        current_post.post=form.post.data
        # db.session.add(current_post)
        db.session.commit()
        return redirect(url_for('.index'))
    elif request.method=='GET':
        form.title.data=current_post.title
        form.category.data=current_post.category
        form.post.data=current_post.post
        
    return render_template('comment.html',form=form)


@main.route('/user/<name>')
def profile(name):

    user=User.query.filter_by(username = name).first()
    user_id=current_user._get_current_object().id
    posts=Pitch.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)
    return render_template("profile/profile.html",user=user,posts=posts)



@main.route('/user/<name>/updateprofile',methods=['GET','POST'])
@login_required
def updateprofile(name):
    
    user=User.query.filter_by(username=name).first()
   
    if user == None:
        abort(404)
    form=UpdateProfile()
    if form.validate_on_submit():
        user.bio=form.bio.data
        # user.save_u()
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',name=user.username))
    return render_template('profile/update.html',form=form)
@main.route('/user/<name>/update/pic',methods=['POST'])
@login_required
def update_pic(name):
    
    user=User.query.filter_by(username=name).first()
   
    if 'photo' in request.files:
        filename=photos.save(request.files['photo'])
        path=f'photos/{filename}'
        user.profile_pic_path=path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))


@main.route('/blog',methods = ['GET','POST'])
@login_required
def add_blog():
    form = BlogForm()
    if form.validate_on_submit():
        article = form.article.data
        category = form.category.data
        new_article = Article(article = article,category = category,user = current_user)
        new_article.save_article()
        return redirect(url_for('.index'))
    title = 'Add a blog'
    return render_template('blog.html',title = title,form = form)
