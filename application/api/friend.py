from flask import Flask, Blueprint, render_template, request, redirect, jsonify,session

from application.db.friend import send_friend_req_db, approve_friend_req_db, get_friend_list_db
from application.db.custom import get_use_custom_db
import json

from application.db.notification import set_notification_db
from application.db.tag import get_tag_list_db

friend = Blueprint('friend', __name__, url_prefix='/api/friend')


@friend.route('/get_friend_list', methods=["POST"])
def get_friend_list():
    primary_user_id = request.json['primary_user_id']
    friend_list = get_friend_list_db(primary_user_id)            
    if friend_list:
        return jsonify(friend_list), 200
    else:
        return jsonify([]), 200

@friend.route('/get_hima_friend_list', methods=["POST"])
def get_hima_friend_list():
    primary_user_id = request.json['primary_user_id']
    friend_list = get_friend_list_db(primary_user_id, only_hima=True)

    koukai_friend_list = []
    for friend in friend_list:
        koukai_list = get_use_custom_db(friend['friend'])
        if len(koukai_list) == 0 or primary_user_id in koukai_list:
            tag_list = get_tag_list_db(friend['friend'])
            friend["tag_list"] = [tag["tag_name"] for tag in tag_list]

            friend_list = get_friend_list_db(friend['friend'])
            friend["friend_list"] = [f["friend"] for f in friend_list]
            koukai_friend_list.append(friend)
            
    if koukai_friend_list:
        return jsonify(koukai_friend_list), 200
    else:
        return jsonify([]), 200

@friend.route('/send_friend_req', methods=["POST"])
def send_friend_req():
    if 'user' in session:
        primary_user_id = session['user']
        friend = request.json['friend']
        send_friend_req_db(primary_user_id, friend)
        #通知を設定する
        set_notification_db(friend, 1, partner=primary_user_id)
        return jsonify(res="ok")
    else:
        return {"error" : "please login"}

@friend.route('/approve_friend_req', methods=["POST"])
def approve_friend_req():
    if 'user' in session:
        primary_user_id = session['user']
        friend = request.json['friend']
        approve_friend_req_db(approver=primary_user_id, approved=friend)

        set_notification_db(friend, 2, partner=primary_user_id)
        return jsonify(res="ok")
    else:
        return {"error" : "please login"}