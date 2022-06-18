import os
from application.db.connect import get_connection
from flask import Flask, render_template, request, jsonify
from datetime import timedelta

app = Flask(__name__)


#sessionの設定
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
)

app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(hours=12)

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

@app.route("/test")
def index_2():
    return render_template('sample.html',users=get_users())

@app.route("/get_profile", methods=["GET"])
def get_profile():
    primary_user_id = 1
    #primary_user_id = request.json["primary_user_id"]
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select * from users where primary_user_id = {primary_user_id}'
    cur.execute(sql)
    user_profiles = cur.fetchall()
    cur.close()
    conn.close()
    return {"user_profiles":user_profiles} #該当ユーザの全カラム取得

