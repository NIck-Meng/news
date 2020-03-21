from app.main import main
from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, make_response, \
    send_from_directory
@main.route("/")
def index():
    return render_template("main/index.html")