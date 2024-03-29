import time
from datetime import datetime
import random
from flask import jsonify, request, g, url_for, current_app
from sqlalchemy import and_

from . import api
from .. import db
from ..models import Feed,News_List

@api.route("/get_feed/<int:num>")
def feed(num):
    import time
    three_days_ago_timestamps = time.time() - 3 * 24 * 60 * 60
    current_timestamps = datetime.utcnow()

    recommends_list = News_List.query \
        .filter(and_(News_List.middle_image != "{}", News_List.behot_time >= three_days_ago_timestamps)) \
        .limit(num).all()

    hot_news_list = News_List.query \
        .filter(and_(News_List.middle_image != "{}", News_List.behot_time >= three_days_ago_timestamps)) \
        .order_by(News_List.read_count.desc()) \
        .limit(num).all()



    # has_more= True
    # message="success"
    # feed = Feed.query.filter_by().limit(num).all()
    # data=[v.to_json() for v in feed]
    # max_behot_time=int(time.time())
    return jsonify(recommends_list=[v.to_json() for v in recommends_list],
                   hot_news_list=[v.to_json() for v in hot_news_list],
                   current_timestamps=current_timestamps
                  )
@api.route("/get_channel/<int:n>")
def get_channel(n):
    rslt=[]
    channel_list=["5G","芯片",'健康','历史','军事','政治','财经','国学','新冠疫情','教育']
    for i in  range(n):
        rslt.append(random.choice(channel_list))
    return jsonify(rslt)