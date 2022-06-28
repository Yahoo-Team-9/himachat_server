# import os
#
# import beaker
# import redis
# from beaker.middleware import SessionMiddleware
# from flask import Flask
# from flask.sessions import SessionInterface
#
# from datetime import timedelta
# from flask_session import Session
#
# session_opts = {
#     'session.type': 'ext:redis',
#     'session.cookie_expires': True,
#     'session.url': REDIS_URL,
#     'session.auto': True,
# }

# #flaskのsessionにbeakerのseesionを保持させるための処理
# class BeakerSessionInterface(SessionInterface):
#     def open_session(self, app, request):
#         return request.environ['beaker.session']
#
#     def save_session(self, app, session, response):
#         return  True


#def create_app(debug=False):

    # app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    # #berkerのsession設定
    # app.session_interface = BeakerSessionInterface()
