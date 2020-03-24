from flask import Flask, request, jsonify
from flask import send_file
from flask.json import JSONEncoder
import requests
import os.path

import singletons
from datatypes import *


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

app.run(port=8080, debug=True)
