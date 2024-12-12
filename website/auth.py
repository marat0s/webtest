from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle the user login process.
    - GET: Render login page.
    - POST: Validate user credentials and log them in.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            # Check the stored hash against the provided password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)

                # If the user is an admin, optionally redirect to admin panel
                # Adjust 'admin_bp.admin_panel' and route name to match your admin setup
                if user.is_admin:
                    return redirect(url_for('admin_bp.admin_panel'))
                else:
                    return redirect(url_for('routes.home'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Username does not exist. Please sign up first.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle the user registration process.
    - GET: Render sign-up page.
    - POST: Validate form data, create a new user, and log them in.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate inputs
        user = User.query.filter_by(username=username).first()

        if user:
            flash('Пользователь уже существует. Пожалуйста выберите другое имя', category='error')
        elif len(username) <= 3:
            flash('Имя должно быть больше 3 символов', category='error')
        elif len(password) <= 3:
            flash('Пароль должен быть больше 3 символов.', category='error')
        else:
            # Create a new user and hash their password
            new_user = User(
                username=username, 
                password=generate_password_hash(password, method='sha256'),
                is_admin=False  # Adjust this if you want the user to be admin by default.
            )
            db.session.add(new_user)
            db.session.commit()

            # Automatically log in the new user and redirect home
            login_user(new_user, remember=True)
            flash('Аккаунт создан успешно!', category='success')
            return redirect(url_for('routes.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    Log out the current user and redirect to the login page.
    """
    logout_user()
    flash('Вы вышли с аккаунта.', category='info')
    return redirect(url_for('auth.login'))
