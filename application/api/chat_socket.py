from flask_socketio import emit, join_room, leave_room
from application import socketio
from application.db.chat import insert_message_db

@socketio.on("join")
def on_join(username, chatRoom):
    join_room(chatRoom)
    print(f"{username} has connected")


@socketio.on('leave')
def on_leave(username, chatRoom):
    leave_room(chatRoom)
    print(f"{username} has left")


@socketio.on("message")
def handle_message(chatRoom, primary_user_id, message):
    insert_message_db(chatRoom, primary_user_id, message)
    emit("message", message, to=chatRoom)