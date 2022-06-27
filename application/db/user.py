import MySQLdb
from application.db.connect import get_connection

def get_profile_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select * from users where primary_user_id = %s'
    cur.execute(sql, (primary_user_id, ))
    user_profiles = cur.fetchall()
    cur.close()
    conn.close()
    return user_profiles

def edit_profile_db(primary_user_id, edited_profile):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update users set user_id = %s, user_name = %s, bio = %s where primary_user_id = %s'
    cur.execute(sql,(edited_profile["user_id"], edited_profile["user_name"], edited_profile["bio"], primary_user_id))
    conn.commit()
    cur.close()
    conn.close()

def upload_file_db(primary_user_id, filename):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update users set user_image_pass = %s where primary_user_id = %s'
    cur.execute(sql,(filename, primary_user_id))
    conn.commit()
    cur.close()
    conn.close()

def create_user_db(user_profile):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into users (user_id , user_name, bio) values(%s, %s, %s)'
    cur.execute(sql,(user_profile["user_id"], user_profile["user_name"], user_profile["bio"]))
    conn.commit()
    cur.close()
    conn.close()