import os
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session, flash, current_app, url_for
from application.db.user import get_profile_db, edit_profile_db, upload_file_db
from werkzeug.utils import secure_filename
from pathlib import Path
from application.db.user import get_profile_db, edit_profile_db, create_user_db

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
    #return jsonify(user_profiles)
    """画像の表示
    file_path = user_profiles[0][3]
    #return file_path
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path)
    #return path
    with open(path, 'rb') as f:
        icon_file = f.read()
    return icon_file
    """
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
    primary_user_id = request.json["primary_user_id"]
    #primary_user_id = 1
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
            upload_file_db(primary_user_id, filename)
            return jsonify(res="ok") #redirect(url_for('download_file', name=filename))
    return jsonify(res="ok")

 # ユーザー作成
@user.route("/create_user", methods=["POST"])
def create_user():
    # user_profile = {"user_id":"same_desu", "user_name":"さめ", "bio":"さめです"}
    user_profile = request.json["user_profile"]
    create_user_db(user_profile)
    return jsonify(res="ok")
