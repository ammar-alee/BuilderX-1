import os.path
import pickle
import random
from datetime import datetime
from glob import glob
from hashlib import md5

BASE_DIR = "proj"
FILES_DIR = os.path.join(BASE_DIR, "files")
META_DIR = os.path.join(BASE_DIR, "metadata")


def ensure_dir(filename):
    folder = os.path.abspath(os.path.dirname(filename))
    os.makedirs(folder, exist_ok=True)

def get_metadata_path(name):
    return os.path.abspath(os.path.join(META_DIR, name) + ".pickle")

def get_metadata(name):
    path = get_metadata_path(name)
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return dict()

def save_file_metadata(name, contentType):
    meta = get_metadata(name)
    meta["id"] = meta.get("id", random.randint(1, 100000))
    meta["name"] = name
    meta["projectId"] = meta.get("projectId", 1)
    meta["created_at"] = datetime.now()
    meta["last_modified"] = datetime.now()
    meta["deleted_at"] = None
    meta["moved"] = 0
    meta["size"] = None
    meta["content_id"] = meta["id"]
    meta["contentType"] = contentType

    ensure_dir(get_metadata_path(name))
    with open(get_metadata_path(name), "wb") as f:
        pickle.dump(meta, f)

def save_file(name, file_object):
    path = os.path.abspath(os.path.join(FILES_DIR, name))
    ensure_dir(path)
    file_object.save(os.path.abspath(os.path.join(FILES_DIR, name)))

def get_files_list():
    return (os.path.relpath(path, FILES_DIR) for path in glob(FILES_DIR + "/**/*", recursive=True) if os.path.isfile(path))

def hash_file(file_path):
    with open(file_path, "rb") as f:
        m = md5()
        m.update(f.read())
        return m.hexdigest()

def get_poll():
    return {
        "/" + f.replace("\\", "/"): hash_file(os.path.join(FILES_DIR, f)) for f in get_files_list()
    }

def prepare_metadata(d):
    if "json" in d.get("contentType", ""):
        d["content"] = open(os.path.join(FILES_DIR, d["name"]), "r").read()
    return d

def get_files_descriptors():
    return [
        prepare_metadata(get_metadata(f)) for f in get_files_list()
    ]
