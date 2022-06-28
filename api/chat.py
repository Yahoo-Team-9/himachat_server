from flask import Blueprint, request
from db.chat import get_group_messages_db


chat = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat.route("/get_group_messages", methods=["GET"])
def get_group_messages():
    group_id = request.json["group_id"]
    message_history = get_group_messages_db(group_id)
    return {"message_history": message_history}