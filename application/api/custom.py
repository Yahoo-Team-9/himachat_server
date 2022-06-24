from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

from application.db.custom import create_custom_db, set_custom_members_db, get_custom_list_db, get_custom_members_db, set_custom_use_flg_db

custom = Blueprint('custom', __name__, url_prefix='/api/custom')

# 指定したカスタム設定のメンバー取得
@custom.route("/get_custom_members", methods=["GET"])
def get_custom_members():
    custom_id = request.json["custom_id"]
    members = get_custom_members_db(custom_id)    

    return {"members": members}


# カスタム作成&指定したメンバーを追加
@custom.route("/create_custom", methods=["POST"])
def create_group():
    if 'user' in session:
        primary_user_id = session['user']

        custom_id = create_custom_db(primary_user_id)

        # added_members = [2, 3, 4]
        allowed_members = request.json["allowed_members"]
        set_custom_members_db(custom_id[0], allowed_members)

        return jsonify(res="ok")
    else:
        return {"error": "please login"}


# 指定したカスタムに指定したメンバーを追加
@custom.route("/update_custom", methods=["POST"])
def update_group():
    custom_id = request.json["custom_id"]
    allowed_members = request.json["allowed_members"]
    set_custom_members_db(custom_id, allowed_members)

    return jsonify(res="ok")

# カスタム設定の一覧を取得
@custom.route("/get_custom_list", methods=["GET"])
def get_custom_list():
    if 'user' in session:
        custom_list = get_custom_list_db(session['user'])
        return jsonify({"custom_list": custom_list})

#どのカスタム設定を利用するかを設定
@custom.route("/set_custom", methods=["POST"])
def set_custom():
    if 'user' in session:
        primary_user_id = session['user']
        custom_id = request.json["custom_id"]
        set_custom_use_flg_db(custom_id, primary_user_id)
        return jsonify(res="ok")
    else:
        return {"error": "please login"}