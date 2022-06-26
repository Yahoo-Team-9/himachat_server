from application.db.connect import get_connection
from flask import Flask, render_template, request, jsonify, session
from application import create_app


app = create_app(debug=True)


@app.route("/")
def index():
    # TODO: 仮セッション
    session['user'] = '5'
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


