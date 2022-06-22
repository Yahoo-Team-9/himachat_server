from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.leisure import set_leisure_time

leisure = Blueprint('leisure', __name__, url_prefix='/api/leisure')

@leisure.route('/set_leisure', methods=["POST"])
def set_leisure():
     """
     [session_user]が暇になった時に最終ログインタイムを変更する
     :return: json
     """
     if 'user' in session:
        status = set_leisure_time(session['user'])

        if status == 0:
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"status": "ERROR"}), 413

