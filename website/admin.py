# website/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import User
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('У вас нет админских прав.', category='error')
        return redirect(url_for('routes.home'))

    if request.method == 'POST':
        # Create new user
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Такой пользователь уже существует.', category='error')
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password, method='sha256'),
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь создан успешно!', category='success')
            return redirect(url_for('admin.admin_panel'))

    users = User.query.all()
    return render_template('admin.html', user=current_user, users=users)

@admin.route('/reset_password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        flash('У вас нет прав на это действие.', category='error')
        return redirect(url_for('routes.home'))

    new_password = request.form.get('new_password')
    user = User.query.get(user_id)
    if user:
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Пароль сброшен!', category='success')
    else:
        flash('Пользователь не найден.', category='error')

    return redirect(url_for('admin.admin_panel'))

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('У вас нет прав на это действие.', category='error')
        return redirect(url_for('routes.home'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален!', category='success')
    else:
        flash('Пользователь не найден.', category='error')

    return redirect(url_for('admin.admin_panel'))

# website/admin.py

@admin.route('/grant_admin/<int:user_id>', methods=['POST'])
@login_required
def grant_admin(user_id):
    if not current_user.is_admin:
        flash('У вас нет прав на это действие.', category='error')
        return redirect(url_for('routes.home'))

    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        flash('Админские права предоставлены!', category='success')
    else:
        flash('Пользователь не найден.', category='error')

    return redirect(url_for('admin.admin_panel'))