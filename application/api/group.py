from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.group import create_group_db, add_member_db, get_group_members_db, get_group_list_db
import json

group = Blueprint('group', __name__, url_prefix='/api/group')

# 指定したグループのメンバー取得
@group.route("/get_group_members", methods=["GET"])
def get_group_members():
    # group_id = 37
    group_id = request.json["group_id"]
    members = get_group_members_db(group_id)    

    return {"members": members}


# グループ作成&指定したメンバーを追加
@group.route("/create_group", methods=["POST"])
def create_group():
    # primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]

    group_id = create_group_db(primary_user_id)

    # added_members = [2, 3, 4]
    added_members = request.json["added_members"]
    add_member_db(group_id[0], [primary_user_id] + added_members)

    return jsonify(res="ok")


# 指定したグループに指定したメンバーを追加
@group.route("/update_group", methods=["POST"])
def update_group():
    group_id = request.json["group_id"]
    added_members = request.json["added_members"]
    add_member_db(group_id, added_members)

    return jsonify(res="ok")

# ユーザが所属しているグループの一覧を返却 (=チャット一覧の返却)
@group.route("/get_group_list", methods=["GET"])
def get_group_list():
    if 'user' in session:
        group_list = get_group_list_db(session['user'])
        return jsonify({"group_list": group_list})