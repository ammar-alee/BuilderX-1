from flask import Flask, request, jsonify
from flask import send_file
from flask.json import JSONEncoder
import requests
import os.path

import singletons
from datatypes import *
from files import *


class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return JSONEncoder.default(self, o)


app = Flask(__name__)
app.json_encoder = CustomJsonEncoder


@app.route("/app/static/media/<path:path>")
def get_media_file(path):
    headers = dict(request.headers)
    headers["Host"] = "builderx.io"
    r = requests.get(
        "https://builderx.io/app/static/media/" + path,
        headers=headers
    )
    return (r.content, r.status_code, dict(r.headers))

@app.route("/app/<path:path>")
def get_file(path):
    local_path = os.path.join("www", path)
    if os.path.exists(local_path):
        return send_file(local_path)
    
    return send_file("www/index.html")

@app.route("/api/get-my-id", methods=["GET", "POST"])
def get_my_id():
    return jsonify({
        "id": singletons.USER.id,
        "user": serialize_user(
            singletons.USER,
            singletons.TEAM,
            singletons.DOMAIN
        )
    })

@app.route("/api/users/<int:pk>")
def get_user_info(pk):
    return jsonify(serialize_user(
            singletons.USER,
            singletons.TEAM,
            singletons.DOMAIN
    ))

@app.route("/api/projects/<pk>")
def get_project_info(pk):
    ses = create_session(
        request.args.get("connection"),
        singletons.USER,
        singletons.PROJECT
    )
    return jsonify(serialize_project(
        singletons.PROJECT,
        ses,
        singletons.TEAM
    ))

@app.route("/api/file-content", methods=["POST"])
def file_content():
    name = request.form.get("name")[1:]
    save_file_metadata(
        name,
        request.form.get("contentType")
    )
    save_file(
        name,
        request.files.get("content")
    )
    
    print(request.form)
    print(request.files)
    return "no"

@app.route("/api/poll", methods=["GET", "POST"])
def poll():
    ses = create_session(
        request.json["session_id"],
        singletons.USER,
        singletons.PROJECT
    )
    return jsonify({
        "messages": [],
        "sessions": serialize_session(ses),
        "project": serialize_project(
            singletons.PROJECT,
            ses,
            singletons.TEAM
        ),
        "files": get_poll()
    })

@app.route("/api/get-files-content/<id>")
def get_file_content(id):
    path = request.args.get("fileName")[1:]
    return send_file(os.path.join("proj/files/", path))

@app.route("/api/files")
def get_files():
    return jsonify({
        "status": False,
        "messages": None,
        "data": get_files_descriptors()
    })


app.run(port=8080, debug=True)
