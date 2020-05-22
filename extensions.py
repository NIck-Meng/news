
import json
# 放在model才行，不知道为什么
# @login_manager.user_loader
# def load_user(user_id):
#     from .app.models import Admin
#     admin=Admin.query.get(int(user_id))
#     return admin

def dict_generator(raw_str:str,key:str):
    raw_str=raw_str.replace("'","\"")
    return json.loads(raw_str)[key]





