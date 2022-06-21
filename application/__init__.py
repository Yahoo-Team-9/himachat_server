import os
from flask import Flask
from flask_socketio import SocketIO
from datetime import timedelta



socketio = SocketIO(cors_allowed_origins='*')

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    # sessionの設定
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
    )

    app.config['JSON_AS_ASCII'] = False
    app.secret_key = os.environ["SECRET_KEY"]
    app.permanent_session_lifetime = timedelta(hours=12)

    from application.api.follow import follow
    from application.api.group import group
    from application.api.chat import chat
    app.register_blueprint(follow)
    app.register_blueprint(group)
    app.register_blueprint(chat)

    socketio.init_app(app)

    return app