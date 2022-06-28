import MySQLdb
from db.connect import get_connection

def insert_message_db(chatRoom, primary_user_id, message):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into chats(group_id, send_user, message) values(%s, %s, %s)'
    cur.execute(sql, (chatRoom, primary_user_id, message))
    conn.commit()

def get_group_messages_db(group_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select send_user, created_at, message from chats where group_id = %s'
    cur.execute(sql, (group_id, ))
    message_history = cur.fetchall()
    cur.close()
    return message_history