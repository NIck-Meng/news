from .app import login_manager
from manage import app
import json
# 放在model才行，不知道为什么
# @login_manager.user_loader
# def load_user(user_id):
#     from .app.models import Admin
#     admin=Admin.query.get(int(user_id))
#     return admin

def dict_generator(raw_str:str):
    raw_str=raw_str.replace("'","\"")
    return json.loads(raw_str)["url"]




env = app.jinja_env
env.filters['dict_generator'] = dict_generator