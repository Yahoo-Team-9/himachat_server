import os
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session, flash, current_app, url_for
from application.db.user import get_profile_db, edit_profile_db
from werkzeug.utils import secure_filename
from pathlib import Path

path = Path(__file__).parent
path /= '../static/img/user_icon'
UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

user = Blueprint('user', __name__, url_prefix='/api/user')

# プロフィール表示(該当ユーザの全カラム取得)
@user.route("/get_profile", methods=["GET"])
def get_profile():
    """
    primary_user_idのユーザー情報を取得するAPI
    :param: json でprimary_user_idを引き渡してください
    :return: json
    """
    # primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]
    user_profiles = get_profile_db(primary_user_id)
    return jsonify({"user_profiles": user_profiles})


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

#画像ファイルのアップロード
@user.route('/upload_file', methods=['POST'])
def upload_file():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return jsonify(res="ok") #redirect(url_for('download_file', name=filename))
    return jsonify(res="ok")

