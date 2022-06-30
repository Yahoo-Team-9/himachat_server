from application.db.connect import get_connection
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO
import os
import redis

from flask import Flask
from datetime import timedelta
from flask_session import Session
from flask_cors import CORS

REDIS_URL = os.environ.get('REDIS_URL')

app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(REDIS_URL)
Session(app)

app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(hours=12)

from application.api.friend import friend
from application.api.group import group
from application.api.chat import chat
from application.api.leisure import leisure
from application.api.user import user
from application.api.custom import custom
from application.api.tag import tag
from application.api.notification import notification

app.register_blueprint(notification)
app.register_blueprint(friend)
app.register_blueprint(group)
app.register_blueprint(chat)
app.register_blueprint(leisure)
app.register_blueprint(user)
app.register_blueprint(custom)
app.register_blueprint(tag)

CORS(
    app,
    supports_credentials=True
)


socketio = SocketIO(app,logger=True, engineio_logger=True, cors_allowed_origins='*')



@app.route("/")
def index():
    # TODO: 仮セッション
    session['user'] = '1'
    return render_template('sample.html', users=get_users())


def get_users():
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select * from users'
    cur.execute(sql)
    users = cur.fetchall()
    cur.close()
    conn.close()

    return users


@app.route("/test")
def index_2():
    return render_template('sample.html', users=get_users())


from flask_socketio import emit, join_room, leave_room,send

# friendsテーブルのfriend_idをroomのidとしている→ 自分の友達に対してリアルタイムな通知を送信できる
@socketio.on("join")
def on_join(username, rooms):
    for room in list(rooms):
        join_room(room)
        print(f"{username} has connected in {room}")


@socketio.on('leave')
def on_leave(username, rooms):
    for room in rooms:
        leave_room(room)
        print(f"{username} has left from {room}")

# 使い方の想定：
# 暇になった(loginしたなど)、もしくは、暇じゃなくなったら、クライアントからここにemit
# 友達は、誰かのhima状態が変わったことがわかる → top画面を更新してもらう
@socketio.on('update_hima_status')
def handle_status(rooms):
    for room in rooms:
        emit("update_hima_status", to=room)