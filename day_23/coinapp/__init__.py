from flask import Flask
from .extensions import db,bcrypt,ma

def __call__(config_object):
    app = Flask(__name__)
    app.config.from_object(config[config_object])

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # register blueprint
    from .api import api
    app.register_blueprint(api,url_prefix="/api")

    return app