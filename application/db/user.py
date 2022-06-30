import MySQLdb
from application.db.connect import get_connection
from application.util.random_string import randomstring


def get_profile_db(primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select * from users where primary_user_id = %s'
    cur.execute(sql, (primary_user_id, ))
    user_profiles = cur.fetchall()
    cur.close()
    conn.close()
    return user_profiles

def edit_profile_db(primary_user_id, edited_profile):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update users set user_id = %s, user_name = %s, bio = %s where primary_user_id = %s'
    cur.execute(sql,(edited_profile["user_id"], edited_profile["user_name"], edited_profile["bio"], primary_user_id))
    conn.commit()
    cur.close()
    conn.close()

def upload_file_db(primary_user_id, filename):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update users set user_image_pass = %s where primary_user_id = %s'
    cur.execute(sql,(filename, primary_user_id))
    conn.commit()
    cur.close()
    conn.close()

def create_user_db(user_profile):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into users (user_id , user_name, bio) values(%s, %s, %s)'
    cur.execute(sql,(user_profile["user_id"], user_profile["user_name"], user_profile["bio"]))
    conn.commit()
    cur.close()
    conn.close()

def set_hima_status_db(primary_user_id, status):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'update users set hima = %s where primary_user_id = %s'
    cur.execute(sql,(status, primary_user_id))
    conn.commit()
    cur.close()
    conn.close()


def set_server_hash(hash):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into server_hash (secret_id) values(%s)'
    cur.execute(sql, (hash,))
    conn.commit()
    cur.close()
    conn.close()

def check_server_hash(hash):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select secret_id from server_hash where secret_id = %s and (created_at + INTERVAL 2 MINUTE) > NOW() and used_flg= 0'
    cur.execute(sql,(hash,))
    secret_id = cur.fetchone()
    print(secret_id)
    sql = 'UPDATE server_hash SET used_flg = 1 WHERE secret_id = %s and (created_at + INTERVAL 2 MINUTE) > NOW()'
    cur.execute(sql, (hash,))
    conn.commit()
    cur.close()
    conn.close()
    return not(secret_id is None)


def get_social_login_db(email,provider,name):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select primary_user_id from social_login_users where email = %s and provider_name = %s'
    cur.execute(sql,(email, provider))
    primary_userid = cur.fetchone()
    cur.close()
    conn.close()
    if  primary_userid is None:
        return set_social_login_users(email,provider,name)


    return primary_userid[0]

def set_social_login_users(email,provider,name):
    conn = get_connection()
    cur = conn.cursor()
    userid = randomstring(15)
    sql = 'insert into users (user_id , user_name, bio) values(%s, %s, %s)'
    cur.execute(sql,(userid, name, ""))
    conn.commit()
    sql = 'select primary_user_id from users where user_id = %s'
    cur.execute(sql,(userid,))
    primary_userid = cur.fetchone()[0]
    sql = 'insert into social_login_users (email, provider_name, primary_user_id) values(%s, %s, %s)'
    cur.execute(sql,(email, provider, primary_userid))
    conn.commit()
    cur.close()
    conn.close()

    return  primary_userid


def set_session_token(secret,primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'insert into secret_user_sessions (secret_id, primary_user_id) values(%s, %s)'
    cur.execute(sql,(secret, primary_user_id))
    conn.commit()
    cur.close()
    conn.close()
    return 0

def get_session_token(token,primary_user_id):
    conn = get_connection()
    cur = conn.cursor()
    sql = 'select primary_user_id from secret_user_sessions where secret_id = %s and primary_user_id =%s AND (created_at + INTERVAL 2 MINUTE) > NOW() AND used_flg= 0'
    cur.execute(sql,(token,primary_user_id))
    primary_user_id = cur.fetchone()

    sql = 'UPDATE secret_user_sessions SET used_flg = 1 WHERE secret_id = %s and primary_user_id =%s'
    cur.execute(sql, (token, primary_user_id))
    conn.commit()
    cur.close()
    conn.close()
    return primary_user_id



