from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session
from application.db.user import get_profile_db, edit_profile_db
#from application import create_app

user = Blueprint('user', __name__, url_prefix='/api/user')

# プロフィール表示(該当ユーザの全カラム取得)
@user.route("/get_profile", methods=["GET"])
def get_profile():
    """
    primary_user_idのユーザー情報を取得するAPI
    :param: json でprimary_user_idを引き渡してください
    :return: json
    """
    primary_user_id = 1
    # primary_user_id = request.json["primary_user_id"]
    user_profiles = get_profile_db(primary_user_id)
    return jsonify({"user_profiles": user_profiles})


# プロフィール編集（画像以外）
@user.route("/edit_profile", methods=["PUT"])
def edit_profile():
    """
    primary_user_idのユーザー情報を編集するAPI
    :param: json でprimary_user_idとedited_profile({column:value, ...})引き渡してください
    :return: json
    """
    primary_user_id = 1
    # primary_user_id = request.json["primary_user_id"]
    
    edited_profile = {"user_id":"Shishamo_big_Love", "user_name":"柳葉魚"}
    # edited_profile = request.json["edited_profile"]
    edit_profile_db(primary_user_id, edited_profile)
    return jsonify(res="ok")