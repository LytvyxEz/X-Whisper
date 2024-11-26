from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.data.data_base.handlers import *
from app.modules import *

other_bp = Blueprint('other', __name__)
login_manager = LoginManager()
login_manager.init_app(other_bp)


@other_bp.route('/all_users')
@login_required
def all_users():
    users = get_users()
    return render_template('all_users.html', users=users)


@other_bp.route('/all_following_users')
@login_required
def all_following_users():
    user_id = current_user.id
    following_ids = get_following_by_user_id(user_id)

    following_users = get_users_by_list_id(following_ids)

    if following_users:
        return render_template('all_following_users.html', users=following_users)
    else:
        flash("You haven't any follows", 'danger')
        return redirect(url_for('other.all_users'))


@other_bp.route('/global')
@login_required
def global_page():
    name = current_user.name
    user_id = current_user.id
    posts = []
    all_post = get_all_posts()

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])
    return render_template('global.html', user_id=user_id, username=name, posts=posts, all_post=all_post)


@other_bp.route('/following')
@login_required
def following():
    name = current_user.name
    user_id = current_user.id
    posts = []
    all_post = get_all_post_by_follower(user_id)

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])
    return render_template('following.html', user_id=user_id, username=name, posts=posts, all_post=all_post)

