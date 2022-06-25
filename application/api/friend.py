from flask import Flask, Blueprint, render_template, request, redirect, jsonify,session

from application.db.friend import send_friend_req_db, approve_friend_req_db, get_friend_list_db
import json

friend = Blueprint('friend', __name__, url_prefix='/api/friend')


@friend.route('/get_friend_list', methods=["GET"])
def get_friend_list():
    primary_user_id = request.json['primary_user_id']
    friend_list = get_friend_list_db(primary_user_id)
    if friend_list:
        return jsonify(friend_list), 200
    else:
        return jsonify([]), 200


@friend.route('/send_friend_req', methods=["POST"])
def send_friend_req():
    if 'user' in session:
        primary_user_id = session['user']
        friend = request.json['friend']
        send_friend_req_db(primary_user_id, friend)
        return jsonify(res="ok")
    else:
        return {"error" : "please login"}

@friend.route('/approve_friend_req', methods=["POST"])
def approve_friend_req():
    if 'user' in session:
        primary_user_id = session['user']
        friend = request.json['friend']
        approve_friend_req_db(approver=primary_user_id, approved=friend)
        return jsonify(res="ok")
    else:
        return {"error" : "please login"}