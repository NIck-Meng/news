from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    email=StringField(label='邮箱',
                      validators=[
                          DataRequired("邮箱不能为空"),
                          Length(1,64,message="邮箱长度错误"),
                          Email("邮箱格式输入错误")
                      ]
                      )
    username=StringField(label='用户名',
                         validators=[
                             DataRequired("用户名不能为空"),
                             Length(1,64)
        ,Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,'
                'numbers,dots or underscores'
                )])
    password=PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='passwords must match')])
    password2=PasswordField('确认密码',validators=[DataRequired()])
    submit=SubmitField('注册')

class LoginForm(FlaskForm):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,64),Email()])
    password=PasswordField('密码',validators=[DataRequired()])
    remember_me=BooleanField('保持登陆')
    submit=SubmitField("登陆")