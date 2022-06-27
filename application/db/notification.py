import MySQLdb

from application.db.connect import get_connection


def get_notification_db(primary_user_id) -> list:
    #TODO: エラー処理をする
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'SELECT  su.notification_type,su.notification_text,su.partner_user_id,su.primary_user_id from pull_notifications as su ' \
          'left join users as mn on su.partner_user_id = mn.primary_user_id where su.primary_user_id =  %s and in_read = 0'
    cur.execute(sql, (primary_user_id,))
    notification_list = cur.fetchall()
    cur.close()

    #取得時に既読状態にする
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'UPDATE pull_notifications SET in_read = 1  ' \
          'where primary_user_id =  %s and in_read = 0'
    cur.execute(sql, (primary_user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return notification_list

def set_notification_db(primary_user_id,notification_type,text='',partner= '') -> int:
    #notification_type: 0:friend_request,1:frend_a,2:hima
    conn = get_connection()
    cur = conn.cursor()

    if partner == '':
        if text == '':
            return  1
        sql = 'INSERT INTO pull_notifications (primary_user_id,notification_type,notification_text) VALUES (%s,%s,%s)'
        cur.execute(sql, (primary_user_id, notification_type, text))
    elif partner != '':
        if not text == '':
            sql = 'INSERT INTO pull_notifications (primary_user_id,partner_user_id,notification_type,notification_text) VALUES (%s,%s,%s,%s)'
            cur.execute(sql, (primary_user_id, partner, notification_type, text))
        else:
            sql = 'INSERT INTO pull_notifications (primary_user_id,notification_type,partner_user_id) VALUES (%s,%s,%s)'
            cur.execute(sql, (primary_user_id, notification_type, partner))
    else:
        cur.close()
        conn.close()
        return  1

    conn.commit()
    cur.close()
    conn.close()
    return 0