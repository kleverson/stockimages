from flask import render_template, flash, redirect

from app import app


class Error:

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/error_404.html', error = e)

    @app.errorhandler(500)
    def application_error(e):
        return render_template('error/error_500.html', error=e)

    @app.errorhandler(401)
    def authorization_error(e):
        flash('Ops! A sua sessào caiu, faça o login novamente!', 'info')
        return redirect('/login')
