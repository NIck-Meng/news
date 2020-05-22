from flask import Flask,render_template,request,session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from extensions import dict_generator

from config import config_own

db=SQLAlchemy()
moment=Moment()
bootstrap=Bootstrap()
toolbar=DebugToolbarExtension()
login_manager=LoginManager()

login_manager.session_protection='strong'
login_manager.login_view='auth.simple_login'


def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config_own[config_name])

    bootstrap.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)

    db.init_app(app)
    db.app=app
    db.create_all(bind=['news'])
    # Feed.generate_fake(50)

    app.jinja_env.filters['dict_generator'] = dict_generator

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app


from .models import Feed