from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from config import config_own

db=SQLAlchemy()




def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config_own[config_name])


    db.init_app(app)
    db.app=app
    db.create_all()
    Feed.generate_fake(50)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app


from .models import Feed