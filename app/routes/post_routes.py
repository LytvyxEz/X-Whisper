from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.data.data_base import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.modules import *

post_bp = Blueprint('post', __name__)
login_manager = LoginManager()
login_manager.init_app(post_bp)


@post_bp.route('/post/<int:id>', methods=['POST', 'GET'])
@login_required
def post(id):
    user_id = current_user.id
    post_data = get_post_by_id(id)
    if not post_data:
        return redirect(url_for('explore'))

    post_author_id = get_user_id_by_post_id(id)
    post_author = get_user_by_id(post_author_id)

    comment_author_id = get_all_author_id_by_comment()
    comment_author = get_users_by_list_id(comment_author_id)

    title = post_data[0]['title']
    content = post_data[0]['content']
    image_url = post_data[0].get('image_url')
    video_url = post_data[0].get('video_url')
    video_url = get_embed_url(video_url)
    comments = get_all_comments_by_post_id(id)
    user_id = current_user.id
    is_post_author = user_id == post_author_id

    for comment in comments:
        comment_author = get_user_by_id(comment['user_id'])
        comment['author_name'] = comment_author['name']
        comment['author_id'] = comment_author['id']

    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            add_comment(user_id, id, comment)
            flash('Your comment has been added!', 'success')
            return redirect(url_for('post.post', id=id))

    return render_template('post.html',
                           title=title, content=content, id=id, comments=comments,
                           post_author=post_author['name'], post_author_id=post_author_id,
                           image_url=image_url, video_url=video_url, user_id=user_id,
                           is_post_author=is_post_author, comment_author=comment_author)


@post_bp.route('/addpost', methods=["GET", "POST"])  # Corrected the decorator
@login_required
def addpost():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)
    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post_img = request.files.get('post_img')
        post_video = request.form.get('post_video')

        if not title or not content:
            flash('Please fill out all required fields.', 'danger')
            return render_template('addpost.html')

        image_url = None

        if post_img:
            image = post_img.filename
            image_path = f'app/static/downloaded_images/{image}'
            post_img.save(image_path)
            image_url = url_for('static', filename=f'downloaded_images/{image}')

        create_new_post(user_id, title, content, image_url, post_video)
        flash('Post created successfully!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('addpost.html', all_post=all_user_posts)


@post_bp.route('/delete_post', methods=['GET', 'POST'])  # Corrected the decorator
@login_required
def delete_post():
    user_id = current_user.id
    all_user_posts = get_all_posts_by_user_id(user_id)
    for post in all_user_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if request.method == 'POST':
        post_title = request.form.get('delete_post')
        if post_title:
            post = get_post_by_title_and_user_id(post_title, user_id)
            if post:
                delete_post_by_id(post['id'])
                flash("Post deleted successfully", 'success')
                return redirect(url_for('post.delete_post'))
            else:
                flash("No post found with that title.", 'danger')
                return redirect(url_for('post.delete_post'))

    return render_template('delete_post.html', user_id=user_id, all_post=all_user_posts)


@post_bp.route('/explore', methods=['POST', 'GET'])  # Corrected the decorator
@login_required
def explore():
    all_posts = get_all_posts()

    for post in all_posts:
        if post.get('video_url'):
            post['video_url'] = get_embed_url(post['video_url'])

    if request.method == 'POST':
        title = request.form.get('explore_input').strip()
        posts_by_title = get_post_by_title_partial(title)

        for post in posts_by_title:
            if post.get('video_url'):
                post['video_url'] = get_embed_url(post['video_url'])

        if posts_by_title:
            return render_template('explore.html', all_post=posts_by_title, search=title)
        else:
            flash('No posts found for the search query.', 'danger')
            return render_template('explore.html', all_post=None, search=title)

    return render_template('explore.html', all_post=all_posts)


@post_bp.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = get_comment_by_id(id)

    if not comment:
        flash("Comment not found.", "danger")
        return redirect(url_for("home.home"))

    post_id = comment[0]['post_id']
    post = get_post_by_id(post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("home.home"))

    comment_owner = comment[0]['user_id']
    user_id = current_user.id

    if comment_owner != user_id:
        flash("You are not the owner of this comment to delete it.", "danger")
        return redirect(url_for("post.post", id=post_id))

    if request.method == 'POST':
        delete_comment_by_id(id)
        flash("Comment deleted successfully.", "success")
        return redirect(url_for("post.post", id=post_id))

    return render_template('delete_comment.html', comment=comment[0], post_id=post_id)