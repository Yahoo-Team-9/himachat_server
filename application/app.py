import os
from application.db.connect import get_connection
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
import ast

app = Flask(__name__)


#sessionの設定
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
)

app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(hours=12)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')

@app.route("/")
def index():
    return render_template('sample.html',users=get_users())

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select * from users'
    cur.execute(sql)
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    return users

#指定したグループのメンバー取得
@app.route("/get_group_members", methods=["GET"])
def get_group_members():
    # group_id = 37
    group_id = request.json["group_id"]
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select primary_user_id from group_users where group_id={group_id}'
    cur.execute(sql)
    members = cur.fetchall()
    cur.close()

    return {"members": members}
    
#グループ作成&指定したメンバーを追加
@app.route("/create_group", methods=["POST"])
def create_group():
    # primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]

    conn = get_connection()
    cur = conn.cursor()
    sql = f'insert into user_groups(group_owner) values({primary_user_id})'
    cur.execute(sql)
    conn.commit()


    cur.execute('select last_insert_id();')
    group_id = cur.fetchone()
    cur.close()

    
    # added_members = [2, 3, 4]
    added_members = ast.literal_eval(request.json["added_members"]) # "[2,3]" -> [2,3]
    add_member(group_id[0], [primary_user_id] + added_members)
    
    return jsonify(res="ok")

#指定したグループに指定したメンバーを追加
@app.route("/update_group", methods=["POST"])
def update_group():
    group_id = request.json["group_id"]
    added_members = ast.literal_eval(request.json["added_members"]) # "[2,3]" -> [2,3]
    add_member(group_id, added_members)
    
    return jsonify(res="ok")

#グループにメンバーを追加
def add_member(group_id, added_members):
    conn = get_connection()
    cur = conn.cursor()
    for member in added_members:
        sql = f'insert into group_users(group_id, primary_user_id) values({group_id}, {member})'
        cur.execute(sql)
        conn.commit()
    cur.close()

@app.route("/test")
def index_2():
    return render_template('sample.html',users=get_users())

#プロフィール表示(該当ユーザの全カラム取得)
@app.route("/get_profile", methods=["GET"])
def get_profile():
    #primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select * from users where primary_user_id = {primary_user_id}'
    cur.execute(sql)
    user_profiles = cur.fetchall()
    cur.close()
    conn.close()
    return {"user_profiles":user_profiles} 

#プロフィール編集（画像以外）
@app.route("/edit_profile", methods=["PUT"])
def edit_profile():
    #primary_user_id = 1
    primary_user_id = request.json["primary_user_id"]
    #edited_profile = {"user_id":"Shishamo_big_Love", "user_name":"柳葉魚"}
    edited_profile = request.json["edited_profile"]
    conn = get_connection()
    cur = conn.cursor()
    for i in edited_profile:
        sql = f'update users set {i} = "{edited_profile[i]}" where primary_user_id = {primary_user_id}'
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    return jsonify(res="ok") 
@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(username + " has entered the room.", to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

@socketio.on("message")
def handle_message(room, message):
    send(message, to=room)
