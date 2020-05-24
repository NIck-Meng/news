from datetime import datetime
from app.main import main
from flask_login import current_user
from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, make_response, \
    send_from_directory
from ..models import News_List
from sqlalchemy import and_
from  extensions import dict_generator

@main.route("/")
def index():
    # if current_user.is_authenticated:
    #     return "is_authenticated"
    import time
    days_ago_timestamps = time.time() - 5 * 24 * 60 * 60
    current_timestamps=datetime.utcnow()

    recommends_list = News_List.query \
        .filter(and_(News_List.middle_image != "{}", News_List.behot_time >= days_ago_timestamps)) \
        .limit(10).all()

    hot_news_list = News_List.query \
        .filter(and_(News_List.middle_image != "{}", News_List.behot_time >= days_ago_timestamps)) \
        .order_by(News_List.read_count.desc()) \
        .limit(4).all()

    return render_template("main/index.html",
                           recommends_list=recommends_list,
                           hotnewslist=hot_news_list,
                           current_time=current_timestamps,
                           channels=["5G","中国芯片"])


