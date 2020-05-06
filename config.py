import os
basedir=os.path.abspath(os.path.dirname(__file__))


class Config:
    # 数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN= True
    # SQLALCHEMY_ECHO = True # 输出执行的sql语句
    SQLALCHEMY_RECORD_QUERIES=True
    FLASK_DB_QUERY_TIMEOUT=0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ="123"
    DEBUG_TB_INTERCEPT_REDIRECTS = False   #Flask_DebugToolbar会默认拦截重定向

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI ="mysql+pymysql://develop:JFKL2kljf$@2(nici23@132.232.30.2/news"


class TestingConfig(Config):
    WTF_CSRF_ENABLED=False
    TESTING=True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/news_test" or \
                             'sqlite:///' + os.path.join(basedir, 'data_test.sqlite')


config_own={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'default':DevelopmentConfig
}
