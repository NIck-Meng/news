from app.auth import auth
from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, make_response, \
    send_from_directory,jsonify
from app import response_code,db
from ..models import User
import re
from datetime import datetime
from .forms import LoginForm,RegisterForm
from flask_login import login_user,current_user,logout_user

@auth.route('/simple_register', methods=['POST',"GET"])
def simple_register():
    form=RegisterForm()
    if form.validate_on_submit():
        print(form.email.data)
        return redirect(url_for("auth.simple_login"))


    return render_template("auth/register.html",form=form)

@auth.route('/simple_login', methods=['POST',"GET"])
def simple_login():
    form=LoginForm()
    if form.validate_on_submit():
        admin=User.query.filter_by(email=form.email.data).first()
        print(admin)
        if admin is not None:
            login_user(admin,remember=True)
            print("success")
            # flash("login success")
            return redirect(url_for("main.index"))
        else:
             print("login failed")

    return render_template("auth/login.html",form=form)

@auth.route('/simple_logout', methods=['POST',"GET"])
def simple_logout():
    logout_user()
    print("have a good night")
    return render_template("main/index.html")



@auth.route('/register', methods=['POST'])
def register():
    """注册
    1.接受参数（手机号，短信验证码，密码明文）
    2.校验参数（判断是否缺少和手机号是否合法）
    3.查询服务器的短信验证码
    4.跟客户端传入的短信验证码对比
    5.如果对比成功，就创建User模型对象，并对属性赋值
    6.将模型数据同步到数据库
    7.保存session,实现状态保持，注册即登录
    8.响应注册结果
    """
    # 1.接受参数（手机号，短信验证码，密码明文）
    # request.json : 封装了json.loads(request.data)
    json_dict = request.json
    mobile = json_dict.get('mobile')
    # smscode_client = json_dict.get('smscode')
    password = json_dict.get('password')

    # 2.校验参数（判断是否缺少和手机号是否合法）
    if not all([mobile, password]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')

    # 3.查询服务器的短信验证码
    # try:
    #     smscode_server = redis_store.get('SMS:' + mobile)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=response_code.RET.DBERR, errmsg='查询短信验证码失败')
    # if not smscode_server:
    #     return jsonify(errno=response_code.RET.NODATA, errmsg='短信验证码不存在')

    # 4.跟客户端传入的短信验证码对比
    # if smscode_client != smscode_server:
    #     return jsonify(errno=response_code.RET.PARAMERR, errmsg='输入短信验证码有误')

    # 对比成功,创建user模板,对属性赋值
    user = User()
    # 给属性赋值
    user.mobile = mobile
    user.nick_name = mobile
    # 密码需要加密后再存储
    # 在模型类中添加一个属性叫做password并添加setter和getter方法,调用setter方法实现对密码的加密
    user.password = password

    # 记录最后一次登录时间,注册成功后直接登录
    user.last_login = datetime.datetime.now()

    try:
        # 把模型数据同步到数据库
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=response_code.RET.DBERR, errmsg='保存注册数据失败')

    # 保存session,实现状态保持,注册成功后就登录
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name

    # 响应结果
    return jsonify(errno=response_code.RET.OK, errmsg='注册成功')


@auth.route('/login', methods=['POST'])
def login():
    '''用户登录'''

    # 获取参数,手机号,密码
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    # 检验参数,是否缺少,是否合法
    if not all([mobile, password]):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='缺少参数')
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='手机号格式错误')

    # 使用手机号查询用户的信息
    try:
        user = User.query.filter(User.mobile == mobile).first()

    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=response_code.RET.DBERR, errmsg='数据库查询错误')

    if not user:
        return jsonify(errno=response_code.RET.PARAMERR, errmsg='用户名或密码错误')
    # 校验用户的密码是否正确
    if not user.check_password(password):
        return jsonify(errno=response_code.RET.PWDERR, errmsg='用户名或密码错误')

    # 把状态保持信息保存到session,完成登录
    # 保存session,实现状态保持,注册成功后就登录
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name
    # 记录最后一次登录时间,注册成功后直接登录
    user.last_login = datetime.datetime.now()
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=response_code.RET.DBERR, errmsg='记录最后一次登录错误')
    # 响应登录结果
    return jsonify(errno=response_code.RET.OK, errmsg='登录成功')

