from flask import Blueprint, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.modules import *
from app.data.data_base.handlers import *

home_bp = Blueprint('home', __name__)

login_manager = LoginManager()
login_manager.init_app(home_bp)


@home_bp.route('/')
@login_required
def home():
    name = current_user.name
    user_id = current_user.id

    all_post = get_all_posts()

    for post in all_post:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    return render_template('index.html',
                           user_id=user_id, username=name, posts=all_post, all_post=all_post)