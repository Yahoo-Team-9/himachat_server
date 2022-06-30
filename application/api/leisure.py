from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.leisure import set_leisure_time
from application.db.user import set_hima_status_db

from flask_cors import cross_origin

leisure = Blueprint('leisure', __name__, url_prefix='/api/leisure')

@leisure.route('/set_leisure', methods=["POST"])
@cross_origin(supports_credentials=True)
def set_leisure():
    """
     [session_user]が暇になった時に最終ログインタイムを変更する
     :return: json
    """
    if 'user' in session:
        status = set_leisure_time(session['user'])
        set_hima_status_db(session["user"], 1)

        if status == 0:
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"status": "ERROR"}), 413
    else:
        return jsonify({"error": "please login "})

