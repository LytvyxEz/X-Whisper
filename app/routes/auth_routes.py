from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.modules import *
from app.data.data_base import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.init_app(auth_bp)


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rem = request.form.get('remember', 'off')
        user = get_users_by_email(email)

        if not user:
            flash("Email doesn't exist", "danger")
            return redirect(url_for('auth.login'))

        user = user[0]

        if check_password_hash(user['password'], password):
            user_obj = User(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                password=user["password"],
                DOB=user["birthday"],
                gender=user["sex"],
                rem=rem
            )
            login_user(user_obj, remember=user_obj.remember())
            return redirect(url_for('home.home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))

    if request.method == 'POST':

        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        DOB = request.form.get('dob')
        gender = request.form.get('gender')
        users_list = get_users()

        valid = validate_email_format(email)

        for user in users_list:
            if user['name'] == name:
                flash('Username is already registered', 'danger')
                return render_template('register.html')

            if user['email'] == email:
                flash('Email is already registered', 'danger')
                return render_template('register.html')

        if not validate_email_format(email):
            flash("Invalid email format", "danger")
            return render_template('register.html')

        if len(password) < 8:
            flash('Your password must have more than 8 characters', 'danger')
            return render_template('register.html')

        if not any(char.isalpha() for char in password):
            flash('Your password must contain at least one letter', 'danger')
            return render_template('register.html')

        if not any(char.isupper() for char in password):
            flash('Your password must contain at least one uppercase letter', 'danger')
            return render_template('register.html')

        if not any(char.islower() for char in password):
            flash('Your password must contain at least one lowercase letter', 'danger')
            return render_template('register.html')

        if not any(char.isdigit() for char in password):
            flash('Your password must contain at least one digit ', 'danger')
            return render_template('register.html')

        if any(char.isspace() for char in password):
            flash("Your password can't contain spaces", 'danger')
            return render_template('register.html')

        special_characters = '!@#$%^&*(),.?":{}|<>'
        special_characters_list = list(special_characters)
        if not any(special_characters_list for special_character in password):
            flash('Your password must contain at least one special character', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash("Passwords don't match", 'danger')
            return render_template('register.html')

        hash_password = generate_password_hash(password)
        add_user_to_users(name, email, hash_password, DOB, gender)

        flash('Registration successful! You can now log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('logout.html')
