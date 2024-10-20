from supabase import create_client, Client
from data.data_base.config import key, url

supabase: Client = create_client(url, key)


def add_user_to_users(name, email, password, birthday, sex):
    data = {
        'name': name,
        'email': email,
        'password': password,
        'birthday': birthday,
        'sex': sex
    }
    response = supabase.table('users').insert(data).execute()


def get_users():
    response = supabase.table('users').select('*').execute()
    return response.data


def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data[0]


def get_users_by_email(email):
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data


def delete_user_from_users(name):
    response = supabase.table('users').delete().eq('name', name).execute()


def create_new_post(user_id, title, content, image_url, video_url):
    data = {
        'user_id': user_id,
        'title': title,
        'content': content,
        'image_url': image_url,
        'video_url': video_url
    }
    response = supabase.table('posts').insert(data).execute()


def delete_post_by_id(post_id):
    response = supabase.table('posts').delete().eq('id', post_id).execute()


def get_all_posts():
    response = supabase.table('posts').select('*').execute()
    return response.data


def get_all_posts_by_user_id(user_id):
    response = supabase.table('posts').select('*').eq('user_id', user_id).execute()
    return response.data


def get_post_by_id(id):
    response = supabase.table('posts').select('*').eq('id', id).execute()
    return response.data


def add_comment(post_id, comment):
    data = {
        'post_id': post_id,
        'comment': comment
    }
    response = supabase.table('comments').insert(data).execute()


def get_all_comments_by_post_id(post_id):
    response = supabase.table('comments').select('*').eq('post_id', post_id).execute()
    return response.data


def delete_comment_by_id(comment_id):
    response = supabase.table('comments').delete().eq('id', comment_id).execute()
    