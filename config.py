import os
basedir=os.path.abspath(os.path.dirname(__file__))


class Config:
    # 数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN= True
    SQLALCHEMY_ECHO = True # 输出执行的sql语句
    SQLALCHEMY_RECORD_QUERIES=True
    FLASK_DB_QUERY_TIMEOUT=0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI ="mysql+pymysql://root:root@localhost/news"


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
