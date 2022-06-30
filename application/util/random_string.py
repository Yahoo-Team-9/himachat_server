import random
import string

import secrets


def randomstring(n):
    """ランダムで安全な文字列を暗号学的に作成する

   Args:
       length (Number): 生成する文字列の長さを指定

   Returns:
       string: 生成された安全な文字列
   """

    letters = string.ascii_letters
    result_str = ''.join(secrets.choice(letters) for i in range(n))
    return result_str
