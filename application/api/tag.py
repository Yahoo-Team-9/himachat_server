from flask import Flask, Blueprint, render_template, request, redirect, jsonify,session
from application.db.tag import create_tag_db, search_tag_db, set_my_tag_db, unset_my_tag_db, get_tag_list_db

tag = Blueprint('tag', __name__, url_prefix='/api/tag')


@tag.route('/create_tag', methods=["POST"])
def create_tag():
    tag_name = request.json['tag_name']
    create_tag_db(tag_name)
    return jsonify(res="ok")


@tag.route('/search_tag', methods=["GET"])
def search_tag():
    keyword = request.json['keyword']
    result = search_tag_db(keyword)
    return jsonify({"result": result})

@tag.route('/set_my_tag', methods=["POST"])
def set_my_tag():
    if "user" in session:
        primary_user_id = session["user"]
        tag_id = request.json["tag_id"]
        set_my_tag_db(primary_user_id, tag_id)
        return jsonify(res="ok")
    else:
        return {"error": "please log in"}

@tag.route('/unset_my_tag', methods=["POST"])
def unset_my_tag():
    if "user" in session:
        primary_user_id = session["user"]
        tag_id = request.json["tag_id"]
        unset_my_tag_db(primary_user_id, tag_id)
        return jsonify(res="ok")
    else:
        return {"error": "please log in"}

@tag.route('/get_tag_list', methods=["GET"])
def get_tag_list():
    primary_user_id = request.json["primary_user_id"]
    tag_list = get_tag_list_db(primary_user_id)
    return jsonify({"tag_list": tag_list})
