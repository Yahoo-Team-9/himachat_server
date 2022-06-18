from application.db.connect import get_connection


def set_follow_db(follow: str, follower: str) -> bool:
    """
    フォロー情報をfollowテーブルに登録する
    :param follow: follow user_id
    :param follower: follower user_id
    :return boolean
    """
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into follows(follow_user,follower_user) values(%s,%s)'
    cur.execute(sql, (follow, follower))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_follow_list_db(user_id: str) ->list :
    """
    :param user_id: フォローしているユーザーを取得するユーザーID
    :return:　取得したユーザーリスト(primary_user_id, user_id, bio)
    """
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select follows.follower_id, users.user_id, users.bio from follows inner join ' \
          'users users on users.primary_user_id = follows.follpwer_id where follows.follow_id = %s'
    cur.execute(sql,(user_id,))
    user_list = cur.fetchall()
    cur.close()
    conn.close()

    return  user_list


