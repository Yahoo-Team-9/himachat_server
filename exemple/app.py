import os
from webbrowser import get
from exemple.db.connect import get_connection
from flask import Flask, render_template
from datetime import timedelta

app = Flask(__name__)

#Session settings

# app.config.update(
#     SESSION_COOKIE_SAMESITE='',
# )

# app.config['JSON_AS_ASCII'] = False
# app.secret_key = os.environ["SECRET_KEY"]
# app.permanent_session_lifetime = timedelta(hours=15)

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

