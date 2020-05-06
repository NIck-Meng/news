from .app import login_manager

# 放在model才行，不知道为什么
# @login_manager.user_loader
# def load_user(user_id):
#     from .app.models import Admin
#     admin=Admin.query.get(int(user_id))
#     return admin