import os
import MySQLdb

def get_connection():
    # 環境変数の取得
    host = os.environ['DATABASE_HOST']
    pw = os.environ['DATABASE_PASS']
    user = os.environ['MYSQL_USER']
    db = os.environ['MYSQL_DATABASE']

    return MySQLdb.connect(user=user, passwd=pw, host=host, db=db,
                           charset="utf8")
