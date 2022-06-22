from flask import Flask, Blueprint, render_template, request, redirect, jsonify,session

from application.db.follow import set_follow_db, un_follow_db, get_follow_list_db, get_follower_list_db
import json

follow = Blueprint('follow', __name__, url_prefix='/api/follow')


@follow.route('/get_follow_list', methods=["POST"])
def get_follow_list():
    """
    user_idがフォローしているユーザーを取得するAPI
    :param: json でuser_idを引き渡してください
    :return: json
    """
    follow_id = request.json['primary_user_id']
    user_list = get_follow_list_db(follow_id)
    if user_list:
        return jsonify(user_list), 200
    else:
        return jsonify([]), 200


@follow.route('/get_follower_list', methods=["POST"])
def get_follower_list():
    """
    primary_user_idをフォローしているユーザーを取得するAPI
    :param: json でprimary_user_idを引き渡してください
    :return: json
    """
    follower_id = request.json['primary_user_id']
    return jsonify(get_follower_list_db(follower_id)), 200


@follow.route('/follow', methods=["POST"])
def set_follow():

    if 'user'  in session:
        follow_id = request.json['primary_user_id']
        res = set_follow_db(session['user'], follow_id)
        if res == 0:
            return jsonify({"status": "OK"}), 200
        elif res == 1:
            return jsonify({"status": "already follow user"}), 200
    else:
        return jsonify({"status": "not session. pls Login your browser"}), 413


@follow.route('/unfollow', methods=["POST"])
def un_follow():

    if 'user'  in session:
        follow_id = request.json['primary_user_id']
        if un_follow_db(session['user'], follow_id):
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"status": "error"}), 413
    else:
        return jsonify({"status": "not session. pls Login your browser"}), 413
