from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    
    mongo.init_app(app)
    bcrypt.init_app(app)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
