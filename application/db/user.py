import MySQLdb
from application.db.connect import get_connection

def get_profile_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select * from users where primary_user_id = {primary_user_id}'
    cur.execute(sql)
    user_profiles = cur.fetchall()
    cur.close()
    conn.close()
    return user_profiles

def edit_profile_db(primary_user_id, edited_profile):
    conn = get_connection()
    cur = conn.cursor()
    for i in edited_profile:
        sql = f'update users set {i} = "{edited_profile[i]}" where primary_user_id = {primary_user_id}'
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


