from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm



@auth.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            next = request.args.get('next')

            if next is None or next.startswith('/'):
                next = url_for('main.index')
            
            return redirect(next)
        flash('Invalid username or password', category='error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['get', 'post'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login', category='success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)