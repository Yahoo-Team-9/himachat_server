import MySQLdb

from application.db.connect import get_connection


def send_friend_req_db(primary_user_id: str, friend: str) -> int:
    """
    友達追加(申請中)をテーブルに追加
    """
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into friends(primary_user_id,friend) values(%s,%s)'
    cur.execute(sql, (primary_user_id, friend))
    conn.commit()
    cur.close()
    conn.close()
    return 0

def approve_friend_req_db(approver, approved):
    conn = get_connection()
    cur = conn.cursor()
    sql = "update friends set approval = 1 where primary_user_id = %s and friend = %s"
    cur.execute(sql, (approved, approver))
    conn.commit()

    sql = "insert into friends(primary_user_id, friend, approval) values(%s, %s, 1)"
    cur.execute(sql, (approver, approved))
    conn.commit()
    cur.close()
    conn.close()

def get_friend_list_db(user_id: str) ->list :
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = '''select friends.friend, users.bio, users.user_id, users.login_at, users.user_image_pass 
    from friends inner join users 
    on users.primary_user_id = friends.friend 
    where friends.primary_user_id = %s and approval = 1'''
    cur.execute(sql,(user_id,))
    user_list = cur.fetchall()
    cur.close()
    conn.close()
    return  user_list

