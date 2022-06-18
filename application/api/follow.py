from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.follow import set_follow_db

follow = Blueprint('home', __name__, url_prefix='/api/follow')


@follow.route('/get_follow_list')
def get_follow_list():
    return  'a'


@follow.route('/get_follower_list')
def get_follower_list():
    return  'a'

@follow.route('/follow', methods=["POST"])
def set_follow():
    #if session not in session
    follow_id = request.form.get('user_id')
    if set_follow_db(session['user'],follow_id):
        return jsonify({"status": "OK"}), 200
    else:
        return  jsonify({"status","not followed"}),413


