import MySQLdb
from application.db.connect import get_connection


def create_custom_db(primary_user_id, custom_name):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into customs(primary_user_id, custom_name) values(%s, %s)'
    cur.execute(sql, (primary_user_id, custom_name))
    conn.commit()

    cur.execute('select last_insert_id();')
    custom_id = cur.fetchone()
    cur.close()

    return custom_id

# 公開するカスタム設定のメンバーを設定
def set_custom_members_db(custom_id, allowed_members):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'delete from custom_users where custom_id = %s'
    cur.execute(sql, (custom_id, ))
    for member in allowed_members:
        sql = 'insert into custom_users(custom_id, allowed_user) values(%s, %s)'
        cur.execute(sql, (custom_id, member))
        conn.commit()
    cur.close()

def get_custom_members_db(custom_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select allowed_user from custom_users where custom_id = %s'
    cur.execute(sql, (custom_id,))
    members = cur.fetchall()
    cur.close()

    return members

def get_custom_list_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select custom_id, custom_name from customs where primary_user_id = %s'
    cur.execute(sql, (primary_user_id,))
    custom_list = cur.fetchall()
    cur.close()

    return custom_list

def set_custom_use_flg_db(custom_id, primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update customs set use_flg = 0 where primary_user_id = %s and use_flg = 1'
    cur.execute(sql, (primary_user_id,))
    conn.commit()

    sql = 'update customs set use_flg = 1 where custom_id = %s'
    cur.execute(sql, (custom_id,))
    conn.commit()
    cur.close()

def get_use_custom_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select custom_id from customs where primary_user_id = %s and use_flg = 1'
    cur.execute(sql, (primary_user_id,))
    custom_id = cur.fetchall()
    cur.close()

    return custom_id

def set_no_use_custom_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update customs set use_flg = 0 where primary_user_id = %s and use_flg = 1'
    cur.execute(sql, (primary_user_id,))
    conn.commit()