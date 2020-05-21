import os
basedir=os.path.abspath(os.path.dirname(__file__))


class Config:
    # 数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN= True
    SQLALCHEMY_RECORD_QUERIES=True
    FLASK_DB_QUERY_TIMEOUT=0.5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY ="123"
    DEBUG_TB_INTERCEPT_REDIRECTS = False   #Flask_DebugToolbar会默认拦截重定向

class OnlineConfig(Config):
    DEBUG=False
    # SQLALCHEMY_DATABASE_URI ="mysql+pymysql://develop:JFKL2kljf$@2(nici23@127.0.0.1/news"


    SQLALCHEMY_BINDS = {
        'news': "mysql+pymysql://develop:JFKL2kljf$@2(nici23@127.0.0.1/news",
        'spider': "mysql+pymysql://develop:JFKL2kljf$@2(nici23@127.0.0.1/spider"
    }



class DevelopingConfig(Config):
    SQLALCHEMY_ECHO = True # 输出执行的sql语句
    DEBUG=True
    # SQLALCHEMY_DATABASE_URI="mysql+pymysql://develop:JFKL2kljf$@2(nici23@132.232.30.2/news_test"

    SQLALCHEMY_BINDS = {
        'news': "mysql+pymysql://develop:JFKL2kljf$@2(nici23@132.232.30.2/news_test",
        'spider': "mysql+pymysql://develop:JFKL2kljf$@2(nici23@132.232.30.2/spider_test"
    }


config_own={
    'online':OnlineConfig,
    'developing':DevelopingConfig,
    'default':DevelopingConfig
}
