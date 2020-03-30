from flask import Flask, request, render_template, jsonify
from flask import send_file
from flask.json import JSONEncoder
import os.path
import json
import webbrowser

from staticfiles import WWW_DIR, fetch_resource
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


@app.route("/app/<path:path>")
def route_static_file(path):
    if os.path.splitext(path)[1] == "" or os.path == "/index.html":
        # They are actually requesting the index page (no extension)
        return render_template(
            "index.html",
            **({
                "local_url": "http://localhost:9089",
                "project_id": os.path.basename(path)
            })
        )
    else:
        return fetch_resource(path)


@app.route("/api/get-my-id")
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
def get_project_pk(pk):
    session = create_session(
        request.args.get("connectionId"),
        singletons.USER,
        pk
    )
    proj = get_project_info(pk)
    return jsonify(serialize_project(
        proj,
        session,
        singletons.TEAM
    ))


@app.route("/api/projects/<pk>", methods=["PUT"])
def put_project_pk(pk):
    return jsonify(update_project_info(pk, request.json))


@app.route("/api/get-files-content/<id>")
def get_file_content(id):
    path = request.args.get("fileName")[1:]
    return send_file(get_project_file_path(id, path))


@app.route("/api/poll", methods=["GET", "POST"])
def poll():
    j = request.json or json.loads(request.data)
    pk = j["project_id"]
    session = create_session(
        j["session_id"],
        singletons.USER,
        pk
    )
    return jsonify({
        "messages": [],
        "sessions": serialize_session(session),
        "project": serialize_project(
            get_project_info(pk),
            session,
            singletons.TEAM
        ),
        "files": get_poll(j["project_id"])
    })


@app.route("/api/file-content", methods=["POST"])
def file_content():
    name = request.form.get("name")[1:]
    save_file_metadata(
        request.form.get("projectId"),
        name,
        request.form.get("contentType")
    )
    save_file(
        request.form.get("projectId"),
        name,
        request.files.get("content")
    )
    return "no"


@app.route("/api/files")
def get_files():
    return jsonify({
        "status": False,
        "messages": None,
        "data": get_files_descriptors(request.args.get("projectId"))
    })


@app.route("/api/files/<int:pk>", methods=["DELETE"])
def remove_file_delete(pk):
    delete_file(pk)
    return "ok"


DEBUG=False
if not DEBUG:
    webbrowser.open("http://localhost:9089/app/project1")

app.run(debug=DEBUG, port=9089)
