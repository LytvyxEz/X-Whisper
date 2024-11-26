from flask import flash, redirect, url_for
from flask_login import LoginManager, UserMixin
from app.data.data_base import *
from email_validator import validate_email, EmailNotValidError


class User(UserMixin):
    def __init__(self, id, email, name, password, DOB, gender, rem=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.DOB = DOB
        self.gender = gender
        self.rem = rem

    def remember(self):
        return self.rem == 'on'

    def get_id(self):
        return str(self.id)


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(id=user['id'], email=user['email'], name=user['name'],
                    password=user['password'], DOB=user['birthday'], gender=user['sex'])
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to be logged in to access this page.", "warning")
    return redirect(url_for('auth.login'))


def validate_email_format(email):
    try:
        valid = validate_email(email)
        return True
    except EmailNotValidError:
        return False


def get_embed_url(video_url):
    if not video_url:
        return None

    if "tiktok.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        return f"https://www.tiktok.com/embed/%7Bvideo_id%7D"

    if "youtube.com" in video_url:
        if "watch?v=" in video_url:
            video_url = video_url.replace("watch?v=", "embed/")
        elif "/shorts/" in video_url:
            video_id = video_url.split("/shorts/")[-1].split('?')[0]
            video_url = f"https://www.youtube.com/embed/%7Bvideo_id%7D"
    elif "youtu.be" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://www.youtube.com/embed/%7Bvideo_id%7D"

    if "&" in video_url:
        video_url = video_url.split("&")[0]

    if "vimeo.com" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
        video_url = f"https://player.vimeo.com/video/%7Bvideo_id%7D"

    return video_url
