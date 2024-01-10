from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user
from flaskblog import db
from flaskblog.models import User
from flaskblog.users.forms import RegisterForm, LoginForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as {user_to_create.username}')
        return redirect(url_for('market.market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                 attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market.market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@users.route('/logout')
def logout_page():
    logout_user()
    flash('You have been successfully logout, Thank You', category='info')
    return redirect(url_for("main.home_page"))