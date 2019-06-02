import binascii
import datetime
import os

import flask
from flask import flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from app import app, bcrypt, lm, mail, db
from forms.formuser import LoginForm, LostFormPassword, RecoverFormPassword, RegisterFormUser

from models.User import RolesUsers,Role,User

class AuthController:
    @lm.user_loader
    def load_user(id):
        return User.query.filter_by(id=id).first()

    @app.route('/login', methods=["GET", "POST"])
    @app.route('/user/login', methods=["GET", "POST"])
    def login():
        form = LoginForm()

        if flask.request.method == "POST" and form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user is None or not user.check_password(form.password.data):
                login_user(user)
                return redirect('/search')
            else:
                flash('Usuário e/ou Senha incorreta', 'error')
                return redirect(url_for('login'))

        return render_template('user/login.html', form=form)

    @app.route('/register', methods=["GET","POST"])
    def register():

        form = RegisterFormUser()

        if flask.request.method == "POST":
            if form.validate_on_submit():
                u = User(
                    name=form.name.data,
                    username=form.email.data,
                    email=form.email.data,
                    created_at=datetime.datetime.now(),
                    modified_at=datetime.datetime.now()
                )
                u.set_token('name-{}'.format(form.name.data))
                u.set_password(form.password.data)
                db.session.add(u)
                db.session.commit()
                flash('success','Cadastro realizado com sucesso!')

                return redirect('/login')
        return render_template('user/register.html', form=form)

    @app.route('/lostpassword', methods=["GET", "POST"])
    def lostpassword():
        form = LostFormPassword()

        if flask.request.method == "POST" and form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user is not None:
                print(user.email)
                email = Message("Recuperar senha", sender='kleverson.holanda@gmail.com', recipients=[user.email])
                email.html = '<a href="{}">Recuperar senha</a>'.format(
                    url_for('recoverpassword', token=user.token, _external=True))
                mail.send(email)
                print(email);
                flash("Confira a caixa de entrada", "success")
                return redirect(url_for('login'))
            else:
                flash('Usuario não encontrado!', "danger")
                return redirect(url_for('login'))

        return render_template('user/lostpassword.html', form=form)

    @app.route('/recoverpassword/<token>', methods=["GET", "POST"])
    def recoverpassword(token):

        if token is not None:
            form = RecoverFormPassword()
            user = User.query.filter_by(token=token).first()

            if user is not None:
                if flask.request.method == "POST" and form.validate_on_submit():
                    user.password = bcrypt.generate_password_hash(str(form.password.data)).decode("utf-8")
                    user.token = binascii.b2a_hex(os.urandom(15)).decode("utf-8")

                    db.session.commit()

                    flash('Senha redefinida com sucesso!', 'info')
                    return redirect(url_for('login'))
            else:
                flash('Token inválido')
                return redirect(url_for('lostpassword'))

            return render_template('user/recoverpassword.html', form=form, token=user.token)

    @app.route('/changepass', methods=["GET", "POST"])
    @login_required
    def profile():
        viewdata = {
            'page_title': 'Trocar senha'
        }
        form = RecoverFormPassword()
        user = User.query.get(flask.session['user_id'])

        if flask.request.method == "POST":
            if form.validate_on_submit():
                user.password = bcrypt.generate_password_hash(str(form.password.data)).decode("utf-8")
                user.token = binascii.b2a_hex(os.urandom(15)).decode("utf-8")

                db.session.commit()

                flash('Perfil editado com sucesso!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Preencha os campos corretamente', 'error')
                return redirect(url_for('profile'))

        else:
            return render_template('user/profile.html', user=user, form=form, data=viewdata)

    @app.route("/logout", methods=["GET"])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))