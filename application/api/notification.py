import json
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.connect import get_connection
from application.db.notification import get_notification_db, set_notification_db

notification = Blueprint('notification', __name__, url_prefix='/api/notification')


@notification.route('/get_pull_notification', methods=['GET'])
def get_pull_notification():
    if 'user' in session:
        primary_user_id = session['user']
        list = get_notification_db(primary_user_id)
        return jsonify(list), 200
    else:
        return jsonify({"error" : "pls login"}),200


@notification.route('/set_pull_notification', methods=['POST'])
def set_pull_notification():
    #手動で通知を作成する場合のルート
    if 'user' in session:
        primary_user_id = session['user']
        type = request.json['type']
        if 'partner' in request.json:
            if 'text' in request.json:
                partner = request.json['partner']
                text = request.json['text']
                stat = set_notification_db(primary_user_id, type,text, partner)
                if stat != 0:
                    return jsonify({"msg": "invalid request"}), 200

                return jsonify({"msg": "ok"}), 200

            partner = request.json['partner']
            stat = set_notification_db(primary_user_id, type,partner=partner)
            if stat != 0:
                return jsonify({"msg": "invalid request"}), 200

            return jsonify({"msg": "ok"}), 200
        elif 'text' in request.json:
                text = request.json['text']
                stat = set_notification_db(primary_user_id, type, text)
                if stat != 0:
                    return jsonify({"msg": "invalid request"}), 200

                return jsonify({"msg": "ok"}), 200
        return jsonify({"msg": "invalid request"}), 200

    else:
        return jsonify({"error" : "pls login"}),200
