import os

import beaker
import redis
from beaker.middleware import SessionMiddleware
from flask import Flask
from flask.sessions import SessionInterface
from flask_socketio import SocketIO
from datetime import timedelta


socketio = SocketIO(cors_allowed_origins='*')

REDIS_URL = os.environ.get('REDIS_URL')


session_opts = {
    'session.type': 'ext:redis',
    'session.cookie_expires': True,
    'session.url': REDIS_URL,
    'session.auto': True,
}

#flaskのsessionにbeakerのseesionを保持させるための処理
class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        return request.environ['beaker.session']

    def save_session(self, app, session, response):
        return  True


def create_app(debug=False):
    app = Flask(__name__)
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    #berkerのsession設定
    app.session_interface = BeakerSessionInterface()
    app.debug = debug

    app.config['JSON_AS_ASCII'] = False
   # app.secret_key = os.environ["SECRET_KEY"]
    app.permanent_session_lifetime = timedelta(hours=12)

    from application.api.follow import follow
    from application.api.group import group
    from application.api.chat import chat
    from application.api.leisure import leisure
    from application.api.user import user
    app.register_blueprint(follow)
    app.register_blueprint(group)
    app.register_blueprint(chat)
    app.register_blueprint(leisure)
    app.register_blueprint(user)

    socketio.init_app(app)
    return app