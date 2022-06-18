import os

from application.api.follow import follow
from application.db.connect import get_connection
from flask import Flask, render_template, session
from datetime import timedelta

app = Flask(__name__)


#sessionの設定
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
)

app.config['JSON_AS_ASCII'] = False
app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(hours=12)


app.register_blueprint(follow)

@app.route("/")
def index():
    #TODO: 仮セッション
    session['user'] = '1'
    return render_template('sample.html',users=get_users())

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select * from users'
    cur.execute(sql)
    users = cur.fetchall()
    cur.close()
    
    return users
