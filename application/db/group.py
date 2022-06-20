from application.db.connect import get_connection


def create_group_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = f'insert into user_groups(group_owner) values({primary_user_id})'
    cur.execute(sql)
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
        sql = f'insert into group_users(group_id, primary_user_id) values({group_id}, {member})'
        cur.execute(sql)
        conn.commit()
    cur.close()

def get_group_members_db(group_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = f'select primary_user_id from group_users where group_id={group_id}'
    cur.execute(sql)
    members = cur.fetchall()
    cur.close()

    return members