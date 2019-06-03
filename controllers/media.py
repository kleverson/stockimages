import datetime
import os
import secrets


import flask
from colorthief import ColorThief
from flask import flash, render_template, redirect, url_for, abort, send_from_directory
from flask.json import jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import app, db
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, PER_PAGE, THUMB_HEIGHT, THUMB_WIDTH, THUMB_FOLDER
from forms.formmedia import FormMediaAdd
from models.Media import Media, Color
from PIL import Image

from models.User import RolesUsers,Role,User


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _uniquefilename(file):
    f = file.split('.')
    return secrets.token_hex(16) + ".{}".format(f[-1])

def _create_thumb(img, filename):
    img.resize((THUMB_WIDTH, THUMB_HEIGHT), Image.BICUBIC)
    img.save(THUMB_FOLDER+"/{}".format(filename))

class MediaController:

    @app.route('/media/add', methods=["GET","POST"])
    @login_required
    def add():

        form = FormMediaAdd()

        return render_template('media/add.html', form = form)

    @app.route('/media/upload', methods=["POST"])
    def upload_media():
        if 'file' not in flask.request.files:
            abort(400)

        file = flask.request.files['file']

        if file.filename == '':
            abort(400)

        if file and _allowed_file(file.filename):
            filename = _uniquefilename(file.filename).lower()

            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = UPLOAD_FOLDER + "/{}".format(filename)

            img = Image.open(filepath)

            _create_thumb(img, filename);
            width, height = img.size

            color_thief = ColorThief(filepath)

            m = Media(
                name="",
                file=filename,
                dominant_color = '#%02x%02x%02x' % color_thief.get_color(quality=1),
                file_type = img.format.lower(),
                resolution = "{}x{}".format(width,height),
                user_id=current_user.get_id(),
                is_public=False,
                created_at=datetime.datetime.now(),
                modified_at=datetime.datetime.now()
            )
            db.session.add(m)
            db.session.commit()

            palette = color_thief.get_palette(color_count=6)

            for c in palette:
                db.session.add(Color(
                    color='#%02x%02x%02x' % c,
                    media_id=m.id,
                    created_at=datetime.datetime.now(),
                    modified_at=datetime.datetime.now()
                ))
                db.session.commit()

            if m.id is not None:
                return jsonify({
                    'status':True
                })
            else:
                return jsonify({
                    'status':False
                })

    @app.route('/media/edit/<int:id>', methods=["GET","POST"])
    def edit(id):
        form = FormMediaAdd()
        data = Media.query.filter_by(id=id).first()
        if int(data.id) > 0:
            form.name.data = data.name
            # form.category.data = int(data.media_category_id)
            form.vertical.data = data.vertical
        return render_template('media/edit.html', form=form)



    @app.route('/uploads/<filename>')
    @app.route('/uploads/thumbs/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)