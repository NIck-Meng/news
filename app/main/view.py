from datetime import datetime
from app.main import main
from flask_login import current_user
from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, make_response, \
    send_from_directory
from ..models import News_List
from sqlalchemy import and_
@main.route("/")
def index():
    # if current_user.is_authenticated:
    #     return "is_authenticated"
    return render_template("main/index.html", titles=["today", "done"],
                           current_time=datetime.utcnow(),
                           channels=["教育","医学"],
                           hotnewslist=["武汉新增病例归零啦","美国确诊病例位列榜首","美国加油"],
                           recommends=["美媒：世界曾因新冠病毒害怕中国，如今反过来了",
                                      "21日唯一本土新增新冠肺炎确诊病例来自广东",
                                      "今晚24时起！国家正式实施！"]

            )


@main.route("/news")
def news():
    return render_template("detail.html",
                           recommends=["美媒：世界曾因新冠病毒害怕中国，如今反过来了",
                                      "21日唯一本土新增新冠肺炎确诊病例来自广东",
                                      "今晚24时起！国家正式实施！"]
                           )

@main.route("/index_js")
def firstpage():
    return render_template("base.html",
                           recommends=["美媒：世界曾因新冠病毒害怕中国，如今反过来了",
                                      "21日唯一本土新增新冠肺炎确诊病例来自广东",
                                      "今晚24时起！国家正式实施！"]
                           )


from  extensions import dict_generator
@main.route("/feed/<int:id>")
def feed(id):
    print(id)
    import time
    current_timestamps=time.time()-3*24*60*60

    recommends_list=News_List.query\
        .filter(and_(News_List.middle_image!="{}",News_List.behot_time>=current_timestamps))\
        .limit(10).all()

    for rec in recommends_list:
        print(dict_generator(rec.media_info,"avatar_url"))

    hot_news_list=News_List.query\
        .filter(and_(News_List.middle_image!="{}",News_List.behot_time>=current_timestamps))\
        .order_by(News_List.read_count.desc())\
        .limit(4).all()

    return render_template("main/index.html",recommends_list=recommends_list,hotnewslist=hot_news_list)