from db.connect import get_connection


def set_leisure_time(primary_user_id) -> int:
    #TODO: エラー処理をする
    conn = get_connection()
    cur = conn.cursor()
    sql = 'UPDATE users SET login_at = NOW() WHERE primary_user_id = %s;'
    cur.execute(sql, (primary_user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return 0