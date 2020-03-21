import time

from flask import jsonify, request, g, url_for, current_app
from . import api
from .. import db
from ..models import Feed

@api.route("/get_feed/<int:num>")
def feed(num):
    has_more= True
    message="success"
    feed = Feed.query.filter_by().limit(num).all()
    data=[v.to_json() for v in feed]
    max_behot_time=int(time.time())
    return jsonify(has_more=has_more,
                   message=message,
                   data=data,
                   next={"max_behot_time":max_behot_time})

