from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# WSGI Middleware
class WSGIMiddleware(object):
    def __init__(self, app, prefix):
	self.app = app
	self.prefix = prefix

    def __call__(self, environ, start_response):
	environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
db = SQLAlchemy(app)

# Load views and models
from app import views
#from app import models
