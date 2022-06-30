import os


import time
import json
import base64
import numpy as np
import cv2
import requests
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session, flash, current_app, url_for
from application.db.user import get_profile_db, edit_profile_db, upload_file_db, create_user_db, set_hima_status_db, \
    set_server_hash, get_social_login_db, check_server_hash, set_session_token, get_session_token
from werkzeug.utils import secure_filename
from pathlib import Path

from application.util.random_string import randomstring
from application.util.sha256 import sha256_text

path = Path(__file__).parent
path /= '../static/img/user_icon'
UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
user = Blueprint('user', __name__, url_prefix='/api/user')


# プロフィール表示(該当ユーザの全カラム取得)
@user.route("/get_profile", methods=["POST"])
def get_profile():
    """
    primary_user_idのユーザー情報を取得するAPI
    :param: json でprimary_user_idを引き渡してください
    :return: json
    """
    # primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]
    user_profiles = get_profile_db(primary_user_id)
    
    #アイコンの取得
    file_path = user_profiles[0][3]
    if file_path == "./":
        path = ""
    else:
        """
        current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
        with open(path, 'rb') as f:
            icon_file = f.read()
        # 画像をbase64に変換
        img_byte = base64.b64encode(icon_file).decode("utf-8")
        """
        path = os.path.join('../static/img/user_icon', file_path)
        
    return jsonify({"user_profiles":user_profiles,"icon_path":path})
    

# プロフィール編集（画像以外）
@user.route("/edit_profile", methods=["POST"])
def edit_profile():
    """
    primary_user_idのユーザー情報を編集するAPI
    :param: json でprimary_user_idとedited_profile({"user_id": ,"user_name": ,"bio": })引き渡してください
    :return: json
    """
    # primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]
    
    # edited_profile = {"user_id":"Shishamo_big_Love", "user_name":"柳葉魚", "bio":"こんばんは！!暇なときはゲームしています！気軽に誘ってね♡"}
    edited_profile = request.json["edited_profile"]
    edit_profile_db(primary_user_id, edited_profile)
    return jsonify(res="ok")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#アイコンのアップロード、編集
@user.route('/upload_file', methods=['POST'])
def upload_file():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    primary_user_id = request.json["primary_user_id"]
    #primary_user_id = 1

    #画像をbase64で受け取ってjpgにデコード
    image = request.json['icon_img']
    file_name = request.json['file_name']
    image_dec = base64.b64decode(image)
    data_np = np.fromstring(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)
    
    if request.method == 'POST':
        if file_name == '':
            return jsonify(res="No selected file")
        if file_name and allowed_file(file_name):
            file_name = secure_filename(file_name)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
            cv2.imwrite(path, decimg)
            upload_file_db(primary_user_id, file_name)
            return jsonify(res="ok") #redirect(url_for('download_file', name=filename))
    return jsonify(res="ok")

 # ユーザー作成
@user.route("/create_user", methods=["POST"])
def create_user():
    # user_profile = {"user_id":"same_desu", "user_name":"さめ", "bio":"さめです"}
    user_profile = request.json["user_profile"]
    create_user_db(user_profile)
    return jsonify(res="ok")


@user.route("/set_hima_status", methods=["POST"])
def set_not_hima():
    if "user" in session:
        primary_user_id = session["user"]
        hima_status = request.json["hima_status"] #1 = hima, 0 = not hima
        set_hima_status_db(primary_user_id, hima_status)
        return jsonify(res="ok")
    else:
        return {"error": "please login"}


@user.route("/get_server_hash", methods=["GET"])
def get_server_hash():
    rstr = randomstring(64)
    hash_256 = sha256_text(rstr,os.environ['HASH'])
    set_server_hash(hash_256)

    return jsonify(res=rstr)



@user.route("/login_auth", methods=["POST"])
def login_auth():
    if not 'email' in request.json:
        return jsonify(res="error request")

    if not  'provider' in request.json:
        return jsonify(res="error request")

    if not 'server_token' in request.json:
        return jsonify(res="error request")

    email  = request.json["email"]
    provider = request.json["provider"]
    server_token = request.json["server_token"]
    name = 'user'
    if  'name' in request.json:
        name = request.json["name"]

    if check_server_hash(server_token):
        get_res =  get_social_login_db(email, provider,name)
        primary_user_id = get_res[0]
        if primary_user_id == -1:
            return jsonify(res="error")
        else:
            secret = randomstring(64)
            set_session_token(secret, primary_user_id)

            return jsonify(session_token=secret, primary_user_id=primary_user_id,new_user=get_res[1])
    return jsonify(res="invalid server token")

@user.route("/set_session", methods=["POST"])
def get_session():
    if not 'session_token' in request.json :
        return jsonify(res="error request")
    if not 'primary_user_id' in request.json :
        return jsonify(res="error request")
    session_token = request.json["session_token"]
    primary_user_id = request.json["primary_user_id"]
    sql_primary_id = get_session_token(session_token,primary_user_id)
    if sql_primary_id:
        session["user"] = sql_primary_id
        return jsonify(res="ok")
    else:
        return jsonify(res="error session set")


