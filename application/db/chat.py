from application.db.connect import get_connection

def insert_message_db(chatRoom, primary_user_id, message):
    conn = get_connection()
    cur = conn.cursor()
    sql = f'insert into chats(group_id, send_user, message) values({chatRoom}, {primary_user_id}, "{message}")'
    cur.execute(sql)
    conn.commit()

def get_group_messages_db(group_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select send_user, created_at, message from chats where group_id={group_id}'
    cur.execute(sql)
    message_history = cur.fetchall()
    cur.close()
    return message_history