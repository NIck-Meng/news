from . import db,constants
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager

class BaseModel(object):
    __bind_key__ = 'news'
    """模型基类，为每个模型补充创建时间与更新时间"""
    created = db.Column(db.DateTime, default=datetime.datetime.now())  # 记录的创建时间
    updated = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())  # 记录的更新时间

# 用户收藏表，建立用户与其收藏新闻多对多的关系
user_collection = db.Table(
    "user_collection",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),  # 新闻编号
    db.Column("news_id", db.Integer, db.ForeignKey("news.id"), primary_key=True),  # 分类编号
    db.Column("create_time", db.DateTime, default=datetime.datetime.now),  # 收藏创建时间
    info={'bind_key': 'news'}
)

user_follows = db.Table(
    "user_fans",
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),  # 被关注人的id
    info={'bind_key': 'news'}
)


class User(db.Model,BaseModel,UserMixin):
    """用户"""
    __tablename__ = "user"
    __bind_key__ = 'news'

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=True)  # 用户昵称
    email=db.Column(db.String(32))
    username = db.Column(db.String(32))
    password=db.Column(db.String(32))
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=True)  # 手机号
    avatar_url = db.Column(db.String(256),nullable=True)  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN")

    # 当前用户收藏的所有新闻
    collection_news = db.relationship("News", secondary=user_collection, lazy="dynamic")  # 用户收藏的新闻
    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    followers = db.relationship('User',
                                secondary=user_follows,
                                primaryjoin=id == user_follows.c.followed_id,
                                secondaryjoin=id == user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')

    # 当前用户所发布的新闻
    news_list = db.relationship('News', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        # 用户密码加密并保存
        self.password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        # 校验加密后的密码
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "avatar_url": constants.QINIU_DOMIN_PREFIX + self.avatar_url if self.avatar_url else "",
            "mobile": self.mobile,
            "gender": self.gender if self.gender else "MAN",
            "signature": self.signature if self.signature else "",
            "followers_count": self.followers.count(),
            "news_count": self.news_list.count()
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "mobile": self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict

    def check_password(self, password):
        """
        用于校验密码
        :param password: 要检验的密码的明文
        :return: 返回校验的结果 True/False
        """
        return check_password_hash(self.password_hash, password)



class News(db.Model,BaseModel):
    __tablename__ = "news"
    __bind_key__ = 'news'
    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))  # 分类id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 当前新闻的作者id

    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    # 当前新闻的所有评论
    comments = db.relationship("Comment", lazy="dynamic")

    def to_review_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "reason": self.reason if self.reason else ""
        }
        return resp_dict

    def to_basic_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "index_image_url": self.index_image_url,
            "clicks": self.clicks,
        }
        return resp_dict

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "comments_count": self.comments.count(),
            "clicks": self.clicks,
            "category": self.category.to_dict(),
            "index_image_url": self.index_image_url,
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict


class Comment(BaseModel, db.Model):
    """评论"""
    __tablename__ = "comment"
    __bind_key__ = 'news'
    id = db.Column(db.Integer, primary_key=True)  # 评论编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # 用户id
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)  # 新闻id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 父评论id
    parent = db.relationship("Comment", remote_side=[id])  # 自关联
    like_count = db.Column(db.Integer, default=0)  # 点赞条数

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "parent": self.parent.to_dict() if self.parent else None,
            "user": User.query.get(self.user_id).to_dict(),
            "news_id": self.news_id,
            "like_count": self.like_count
        }
        return resp_dict

class CommentLike(BaseModel, db.Model):
    """评论点赞"""
    __tablename__ = "comment_like"
    __bind_key__ = 'news'
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)  # 用户编号


class Category(BaseModel, db.Model):
    """新闻分类"""
    __tablename__ = "category"
    __bind_key__ = 'news'
    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    news_list = db.relationship('News', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name
        }
        return resp_dict



class Feed(db.Model):
    __tablename__ = 'Feed'
    __bind_key__ = 'news'
    id=db.Column(db.Integer,primary_key=True)
    chinese_tag=db.Column(db.String(64),default="1")
    media_avatar_url=db.Column(db.String(64),default="www.toutiao.com")
    is_feed_ad=db.Column(db.Boolean)
    tag_url=db.Column(db.String(64))
    title=db.Column(db.String(64),default="1")
    single_mode=db.Column(db.Boolean)
    middle_mode=db.Column(db.Boolean)
    abstract=db.Column(db.String(64),default="1")
    tag=db.Column(db.String(64),default="1")
    behot_time=db.Column(db.DateTime)
    source_url=db.Column(db.String(64))
    source=db.Column(db.String(64))
    more_mode=db.Column(db.Boolean)
    article_genre=db.Column(db.String(64))
    comments_count=db.Column(db.Integer,default=1)
    group_source=db.Column(db.Integer)
    item_id=db.Column(db.String(64))
    has_gallery=db.Column(db.Boolean)
    group_id=db.Column(db.String(64))
    media_url=db.Column(db.String(64),default="1")

    def __repr__(self):
        return "<id={0} Feed >".format(self.id)

    def to_json(self):
        feed={
            "chinese_tag": self.chinese_tag,
            "media_avatar_url": self.media_avatar_url,
            "is_feed_ad": self.is_feed_ad,
            "tag_url": self.tag_url,
            "title": self.title,
            "single_mode": self.single_mode,
            "middle_mode": self.middle_mode,
            "abstract": self.abstract,
            "tag": self.tag,
            "behot_time": self.behot_time,
            "source_url": self.source_url,
            "source": self.source,
            "more_mode": self.more_mode,
            "article_genre": self.article_genre,
            "comments_count": self.comments_count,
            "group_source": self.group_source,
            "item_id": self.item_id,
            "has_gallery": self.has_gallery,
            "group_id": self.group_id,
            "media_url": self.media_url
        }
        return feed




    #生成一些虚拟数据
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        seed()
        import forgery_py
        for i in range(count):
            feed = Feed.query.filter_by(id=i + 1).first()
            if feed is None:
                u=Feed(
                # id=db.Column(db.Integer, primary_key=True)
            chinese_tag =forgery_py.personal.race(), #  "中文标签"
            media_avatar_url =forgery_py.internet.domain_name(),
            is_feed_ad=forgery_py.basic.boolean(),
            tag_url=forgery_py.internet.domain_name(),
            title =forgery_py.personal.language(),
            single_mode=forgery_py.basic.boolean(),
            middle_mode=forgery_py.basic.boolean(),
            abstract = forgery_py.lorem_ipsum.title(),
            tag = forgery_py.internet.first_name(),
            behot_time=forgery_py.date.datetime(),
            source_url=forgery_py.internet.domain_name(),
            source=forgery_py.name.company_name(),
            more_mode=forgery_py.basic.boolean(),
            article_genre=forgery_py.lorem_ipsum.title(),
            comments_count = forgery_py.basic.number(),
            group_source=forgery_py.basic.number(),
            item_id=forgery_py.basic.number(),
            has_gallery=forgery_py.basic.boolean(),
            group_id=forgery_py.basic.number(),
            media_url = forgery_py.internet.domain_name()
                   )

                db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

class News_List(db.Model):
    __tablename__='news_list'
    __bind_key__ = 'spider'

    id = db.Column(db.String(256), primary_key=True,autoincrement=True)
    item_id = db.Column(db.String(50), nullable=False)
    abstract = db.Column(db.String(500), nullable=False)
    article_url = db.Column(db.String(200), nullable=False)
    type_name = db.Column(db.String(20), nullable=False)
    user_info = db.Column(db.String(500), nullable=False)
    comment_count = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    hot = db.Column(db.String(11), nullable=False)
    behot_time = db.Column(db.String(11), nullable=False)
    media_info = db.Column(db.String(500), nullable=False)
    media_name = db.Column(db.String(50), nullable=False)
    middle_image = db.Column(db.String(500), nullable=False)
    publish_time = db.Column(db.String(50), nullable=False)
    read_count = db.Column(db.Integer, nullable=False)
    repin_count = db.Column(db.Integer, nullable=False)
    share_count = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

    def to_json(self):
        return {
            "item_id": self.item_id,
            "abstract": self.abstract,
            "article_url": self.article_url,
            "type_name": self.type_name,
            "user_info": self.user_info,
            "comment_count": self.comment_count,
            "group_id": self.group_id,
            "day": self.day,
            "hot": self.hot,
            "behot_time": self.behot_time,
            "media_info": self.media_info,
            "media_name": self.media_name,
            "middle_image": self.middle_image,
            "publish_time": self.publish_time,
            "read_count": self.read_count,
            "repin_count": self.repin_count,
            "share_count": self.share_count,
            "tag": self.tag,
            "title": self.title,
            "created": self.created
        }








@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user