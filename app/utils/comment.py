# _*_ coding:utf-8 _*_

from flask import session, current_app, g
from ..models import User
from functools import wraps

'''
公共的工具文件
'''


def do_rank(index):
    '''自定义过滤器,根据index返回first,second,third'''
    if index == 1:
        return 'first'
    elif index == 2:
        return 'second'
    elif index == 3:
        return 'third'
    else:
        return ''
        # return ['', 'first', 'second', 'third'][index]


# 定义装饰器用于获取用户的登录信息
def user_login_data(view_func):
    '''使用装饰器获取用户登录信息'''

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        '''获取用户的登录信息'''
        user_id = session.get('user_id', None)
        user = None
        if user_id:
            try:
                user = User.query.get(user_id)

            except Exception as e:
                current_app.logger.error(e)
        # 保存user信息
        g.user = user
        return view_func(*args, **kwargs)

    return wrapper
