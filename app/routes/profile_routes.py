from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.data.data_base import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.modules import *

profile_bp = Blueprint('profile', __name__)
login_manager = LoginManager()
login_manager.init_app(profile_bp)


@profile_bp.route('/profile')
@login_required
def profile():
    name = current_user.name
    user_id = current_user.id
    email = current_user.email
    DOB = current_user.DOB
    gender = current_user.gender
    password = current_user.password
    posts = []
    all_user_posts = get_all_posts_by_user_id(user_id)

    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    return render_template('profile.html',
                           username=name, email=email, DOB=DOB, gender=gender, user_id=user_id,
                           posts=posts, all_post=all_user_posts)


@profile_bp.route('/view_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def view_profile(id):
    user = get_user_by_id(id)
    all_posts = get_all_posts_by_user_id(id)
    user_id = current_user.id
    is_following_status = checking_if_user_is_follower(user_id, id)

    for post in all_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if user:
        if request.method == 'POST':
            if is_following_status:
                remove_follower(user_id, id)
                flash('You have unfollowed this user.', 'success')
            else:
                add_new_follower(user_id, id)
                flash('You are now following this user.', 'success')

            return redirect(url_for('profile.view_profile', id=id))

        return render_template('view.html', name=user['name'],
                               id=id, birthday=user['birthday'], sex=user['sex'],
                               all_post=all_posts, is_following=is_following_status,
                               idol=id, user_id=user_id)
    else:
        flash("That user doesn't exist", 'danger')
        return redirect(url_for('home.home'))
