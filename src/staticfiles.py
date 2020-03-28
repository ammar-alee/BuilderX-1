from flask import send_from_directory, send_file
import requests
import os.path

WWW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "www"))

def fetch_resource(path):
    realpath = os.path.join(WWW_DIR, path)

    if not os.path.exists(realpath):
        r = requests.get(
            "https://builderx.io/app/" + path,
            headers={
                "Host": "builderx.io"
            }
        )

        if r.status_code != 200:
            return r.content, r.status_code, dict(r.headers)

        os.makedirs(os.path.dirname(realpath), exist_ok=True)
        with open(realpath, "wb") as f:
            f.write(r.content)

    return send_file(realpath)
