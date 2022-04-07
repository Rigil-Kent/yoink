from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth import auth
from app.email import send_email
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm



@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

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

        token = user.generate_confirmation_token()

        send_email(user.email, 'Confirm Your Yo!nk Account', 'auth/email/confirm', user=user, token=token)

        flash(f'A confirmation email was sent to {user.email}', category='success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        db.session.commit()
        flash('Your account has been confirmed. Thank you!')
    else:
        flash('Invalid or expired confirmation link')

    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()

    send_email(current_user.email, 'Confirm Your Yo!nk Account', 'auth/email/confirm', user=current_user, token=token)

    flash(f'A new confirmation email was sent to {current_user.email}', category='success')

    return redirect(url_for('main.index'))


# TODO: password updates
# TODO: password reset
# TODO: email updates