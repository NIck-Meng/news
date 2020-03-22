from datetime import datetime
from app.main import main
from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, make_response, \
    send_from_directory
@main.route("/")
def index():
    return render_template("main/index_copy.html",titles=["today","done"],
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