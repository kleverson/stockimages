import os

DEBUG=True
ENV = 'development'

TESTING = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
SQLALCHEMY_TRACK_MODIFICATIONS=True
SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/stockimages'


SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_REGISTERABLE = True

UPLOAD_FOLDER = './uploads/full'
THUMB_FOLDER = './uploads/thumbs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc','docx'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
THUMB_WIDTH=450
THUMB_HEIGHT=320

MAIL_SERVER= 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'kleverson.holanda@gmail.com'
MAIL_PASSWORD = 'pljpma@127'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

#Application settings
APP_NAME = "Flask-User starter app"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = True

PER_PAGE = 10