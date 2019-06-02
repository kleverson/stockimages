import flask
from flask_login import current_user

from app import app, lm
from flask import render_template, redirect,request, url_for

from config import PER_PAGE
from forms.formuser import LoginForm
from models import User
from models.Media import Media


class HomeController:

    @app.route("/")
    def home():

        return redirect('/search')

        # form = LoginForm()
        #
        # if current_user.is_authenticated:
        #     redirect(url_for('search'))
        # else:
        #     redirect('/user/login')
        # return render_template('search/index.html', form = form)


    @app.route('/search', methods=["GET"])
    def search():

        page = 1;
        if 'page' in request.args:
            page = int(request.args.get("page"))

        if 'name' in request.args:

            filter['name'] = request.args.get('name')


        medias = Media.query.filter_by( Media.is_public==True ).paginate(page, PER_PAGE, error_out=False)


        return render_template('search/index.html', medias = medias)