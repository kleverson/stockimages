import flask
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination

from app import app, lm, db
from flask import render_template, redirect, request, url_for, flash, abort

from config import PER_PAGE
from forms.formmedia import FormSearchMedia
from forms.formuser import LoginForm
from models import User
from models.Media import Media, Category


class SearchController:

    @app.route('/', defaults={'type':None }, methods=["GET"])
    @app.route('/search', defaults={'type':None }, methods=["GET"])
    @app.route('/search/<string:type>', methods=["GET"])
    def search(type):

        form = FormSearchMedia()
        query = Media.query

        formaction = '/search' if type is None else '/search/my'

        if type is not None and current_user.is_anonymous:
            abort(401)

        if type is None:
            query = query.filter(Media.is_public == True)

        if 'name' in request.args:
            form.name.data = request.args.get('name')
            query = query.filter(Media.name.like("%{}%".format(request.args.get('name'))))

        if 'category' in request.args:
            form.category.data = int(request.args.get('category'))
            query = query.filter(Media.category_id == request.args.get('category'))

        if 'resolution' in request.args:
            query = query.filter(Media.resolution.contains(request.args.get('resolution')))

        if 'owner' in request.args and type is None:
            query = query.filter(Media.user_id == request.args.get('owner'))
        elif type is not None:
            query = query.filter(Media.user_id == current_user.get_id())

        if 'is_vertical' in request.args:
            form.vertical.data = request.args.get('is_vertical')
            query = query.filter(Media.vertical == request.args.get('vertical'))

        page = int(request.args.get("page")) if 'page' in request.args else 1;

        medias = query.paginate(page,PER_PAGE)


        print(form)

        return render_template('search/index.html', medias = query.paginate(page,PER_PAGE), formaction= formaction , form=form)