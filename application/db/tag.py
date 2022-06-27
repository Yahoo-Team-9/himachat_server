import MySQLdb
from application.db.connect import get_connection


def create_tag_db(tag_name):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into tags(tag_name) values(%s)'
    cur.execute(sql, (tag_name, ))
    conn.commit()
    cur.close()

#すでに作られてるタグの中から検索
def search_tag_db(keyword):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select tag_id, tag_name from tags where tag_name like %s'
    cur.execute(sql, ("%"+keyword+"%", ))
    result = cur.fetchall()
    cur.close()

    return result

def set_my_tag_db(primary_user_id, tag_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into user_tags(primary_user_id, tag_id) values(%s, %s)'
    cur.execute(sql, (primary_user_id, tag_id))
    conn.commit()
    cur.close()

def unset_my_tag_db(primary_user_id, tag_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'delete from user_tags where primary_user_id = %s and tag_id = %s'
    cur.execute(sql, (primary_user_id, tag_id))
    conn.commit()
    cur.close()

def get_tag_list_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = '''select tags.tag_id, tags.tag_name
    from user_tags inner join tags
    on user_tags.tag_id = tags.tag_id
    where user_tags.primary_user_id = %s
    '''
    cur.execute(sql, (primary_user_id, ))
    result = cur.fetchall()
    cur.close()

    return result
