from . import db



class Feed(db.Model):
    __tablename__ = 'Feed'
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
