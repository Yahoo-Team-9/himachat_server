import MySQLdb

from application.db.connect import get_connection


def set_follow_db(follow: str, follower: str) -> int:
    """
    フォロー情報をfollowテーブルに登録する
    :param follow: follow user_id
    :param follower: follower user_id
    :return boolean
    """
    conn = get_connection()
    cur = conn.cursor()
    #存在チェック
    sql = 'select follower_user from follows where follow_user = %s and follower_user = %s'
    cur.execute(sql, (follow, follower))
    if cur.fetchall(): return 1
    cur = conn.cursor()
    sql = 'insert into follows(follow_user,follower_user) values(%s,%s)'
    cur.execute(sql, (follow, follower))
    conn.commit()
    cur.close()
    conn.close()
    return 0

def un_follow_db(follow: str, follower: str) -> bool:
    """
    フォロー情報をfollowテーブルから削除する（アンフォロー機能)
    :param follow: follow user_id
    :param follower: follower user_id
    :return boolean
    """
    conn = get_connection()
    cur = conn.cursor()
    sql = 'delete from follows where follow_user = %s and follower_user= %s'
    cur.execute(sql, (follow, follower))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_follow_list_db(user_id: str) ->list :
    """
    :param user_id: 自分がフォローしているユーザーを取得するユーザーID
    :return:　取得したユーザーリスト(primary_user_id, user_id, bio)
    """
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = '''select follows.follower_user, users.bio, users.user_id, users.login_at, users.user_image_pass from follows inner join 
          users users on users.primary_user_id = follows.follower_user where follows.follow_user = %s'''
    cur.execute(sql,(user_id,))
    user_list = cur.fetchall()
    cur.close()
    conn.close()
    return  user_list

def get_follower_list_db(user_id: str) ->list :
    """
    :param user_id: 自分がフォローされているユーザーを取得するユーザーID
    :return:　取得したユーザーリスト(primary_user_id, user_id, bio)
    """
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = '''select follows.follow_user, users.bio, users.user_id, users.login_at, users.user_image_pass from follows inner join 
          users users on users.primary_user_id = follows.follow_user where follows.follower_user = %s'''
    cur.execute(sql,(user_id,))
    user_list = cur.fetchall()
    cur.close()
    conn.close()
    return  user_list

