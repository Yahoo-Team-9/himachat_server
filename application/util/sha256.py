import hashlib


def sha256_text(text, salt=""):
    """与えられた文字列をSHA-256に変換する

   Args:
       text (string): ハッシュ化したい文字
       salt (string): ソルト

   Returns:
       string: 変換後の文字列(16進数)
       textが空の時は　None

   ソルトが存在しない場合、textのみでハッシュ値を生成する。

   """
    if salt is None:
        salt = ''
    print(text)
    print(salt)
    try:
        output = hashlib.pbkdf2_hmac("sha256", bytes(text, 'utf-8'), bytes(salt, 'utf-8'), 5290).hex()

    except NameError:
        print('textが空です。')
        return None

    return output