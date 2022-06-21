import MySQLdb
from application.db.connect import get_connection


def create_group_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into user_groups(group_owner) values(%s)'
    cur.execute(sql, (primary_user_id, ))
    conn.commit()

    cur.execute('select last_insert_id();')
    group_id = cur.fetchone()
    cur.close()

    return group_id

# グループにメンバーを追加
def add_member_db(group_id, added_members):
    conn = get_connection()
    cur = conn.cursor()
    for member in added_members:
        sql = 'insert into group_users(group_id, primary_user_id) values(%s, %s)'
        cur.execute(sql, (group_id, member))
        conn.commit()
    cur.close()

def get_group_members_db(group_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select primary_user_id from group_users where group_id = %s'
    cur.execute(sql, (group_id,))
    members = cur.fetchall()
    cur.close()

    return members