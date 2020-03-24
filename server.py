from flask import Flask, request, jsonify
from flask import send_file
import requests
import os.path

import singletons
from datatypes import serialize_user

app = Flask(__name__)

@app.route("/app/media/<path:path>")
def get_media_file(path):
    headers = dict(request.headers)
    headers["Host"] = "builderx.io"
    r = requests.get(
        "https://builderx.io/app/" + path,
        headers=headers
    )
    return (r.content, r.status_code, dict(r.headers))

@app.route("/app/<path:path>")
def get_file(path):
    local_path = os.path.join("www", path)
    print("Trying to serve file " + local_path)
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


app.run(port=8080, debug=True)
