from flask import render_template,url_for,abort,redirect,request
from . import main
from flask_login import login_user,login_required,current_user
# from .forms import RegistrationForm,LoginForm
from ..models import User,Pitch,Comment,Upvote,Downvote,Category
from .. import db,photos
from .forms import UpdateProfile,PitchForm,CommentForm,CategoryForm



@main.route('/')
def index():
    pitches=Pitch.query.all()
    job=Pitch.query.filter_by(category='Job').all()
    music=Pitch.query.filter_by(category='Music').all()
    news=Pitch.query.filter_by(category='News').all()
    # category=Category.get_categories()
    # return render_template('index.html',category=category)

    return render_template('index.html',job=job,music=music,pitches=pitches,news=news)

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
        new_comment=Comment(comment=comment,user_id=user_id,pitch_id=pitch_id)
        new_comment.save_c()
        
        return redirect(url_for('.comment',pitch_id=pitch_id))
    return render_template('comment.html',form=form,pitch=pitch,all_comments=all_comments)

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

@main.route('/like/<int:id>',methods=['GET','POST'])
@login_required
def like(id):

    get_pitches=Upvote.get_upvotes(id)
    valid_string= f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str=f'{pitch}'
        print(valid_string+ " "+ to_str)

        if valid_string==to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote=Upvote(user=current_user,pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods=['GET','POST'])
@login_required
def dislike(id):

    pitch=Downvote.get_downvotes(id)
    valid_string= f'{current_user.id}:{id}'
    for p in pitch:
        to_str=f'{p}'
        print(valid_string+ " "+ to_str)

        if valid_string==to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote=Downvote(user=current_user,pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id=id))


# @main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
# @login_required
# def new_review(id):
#     form = ReviewForm()
#     movie = get_movie(id)
#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data

#         # Updated review instance
#         new_review = Review(movie_id=movie.id,movie_title=title,image_path=movie.poster,movie_review=review,user=current_user)

#         # save review method
#         new_review.save_review()
#         return redirect(url_for('.movie',id = movie.id ))

#     title = f'{movie.title} review'
#     return render_template('new_review.html',title = title, review_form=form, movie=movie)
@main.route('/category',methods=['GET','POST'])
@login_required
def new_category():
    form=CategoryForm()
    if form.validate_on_submit():
        title=form.title.data
        post=form.post.data
        # category=form.category.data
        user_id=current_user
        new_category_object=Category(post=post,user_id=current_user._get_current_object().id,title=title)
        new_category_object.save_p()
        return redirect(url_for('main.index'))
    return render_template('category.html',form=form)

# @main.route('/review/<int:id>')
# def single_review(id):
#     review=Review.query.get(id)
#     if review is None:
#         abort(404)
#     format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
#     return render_template('review.html',review = review,format_review=format_review)                                                                                         