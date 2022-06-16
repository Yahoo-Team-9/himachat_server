import os
from application.db.connect import get_connection
from flask import Flask, render_template, request, Response
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
    
    return users

@app.route("/get_group", methods=["GET"])
def get_group():
    group_id = 37
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select primary_user_id from group_users where group_id={group_id}'
    cur.execute(sql)
    members = cur.fetchall()
    cur.close()

    return {"members": members}
    

@app.route("/create_group", methods=["POST"])
def create_group():
    primary_user_id = 1
    # primary_user_id = request.form["primary_user_id"]

    conn = get_connection()
    cur = conn.cursor()
    sql = f'insert into user_groups(group_owner) values({primary_user_id})'
    cur.execute(sql)
    conn.commit()

    cur.execute('select last_insert_id();')
    group_id = cur.fetchone()

    
    added_members = [2, 3, 4]
    # added_members = request.form["added_members"]
    for member in [primary_user_id] + added_members:
        sql = f'insert into group_users(group_id, primary_user_id) values({group_id[0]}, {member})'
        cur.execute(sql)
        conn.commit()


    cur.close()
    return Response(status=200)