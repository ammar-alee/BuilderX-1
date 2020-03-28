from datetime import datetime
import os.path
import pickle
from glob import glob
from hashlib import md5
import random

PROJECTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "proj"))

def project_exists(name):
    return os.path.exists(os.path.join(PROJECTS_DIR, name))

def create_project(name):
    project_path = os.path.join(PROJECTS_DIR, name)
    os.makedirs(project_path, exist_ok=True)

    project_info = {
        "id": name,
        "userId": "1",
        "name": name,
        "teamId": "1",
        "ownerId": None,
        "shareability": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None,
        "last_edited_by": None,
        "sample": 0,
        "last_thumbnail_generated_at": datetime.now(),
        "last_edited_at": datetime.now(),
        "access": {
            "access": "write",
            "mode": "design_code",
        },
        "isEditable": True
    }

    with open(os.path.join(project_path, "metadata.pickle"), "wb") as f:
        pickle.dump(project_info, f)

    return project_info


def get_project_info(name):
    if project_exists(name):
        try:
            with open(os.path.join(PROJECTS_DIR, name, "metadata.pickle"), "rb") as f:
                b = pickle.load(f)
                return b
        except FileNotFoundError:
            return create_project(name)
        except pickle.UnpicklingError:
            return create_project(name)

    else:
        return create_project(name)


def update_project_info(name, info):
    inf = get_project_info(name)
    inf.update(info)
    
    with open(os.path.join(PROJECTS_DIR, name, "metadata.pickle"), "wb") as f:
        pickle.dump(inf, f)

    return inf


def get_project_file_path(project_id, file_path):
    return os.path.abspath(os.path.join(PROJECTS_DIR, project_id, "files", file_path))


def ensure_dir(filename):
    folder = os.path.abspath(os.path.dirname(filename))
    os.makedirs(folder, exist_ok=True)


def get_metadata_path(project, filename):
    return os.path.abspath(os.path.join(PROJECTS_DIR, project, "metadata", filename + ".pickle"))


def get_metadata(project, filename):
    path = get_metadata_path(project, filename)
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return dict()


def save_file_metadata(project, filename, contentType):
    meta = get_metadata(project, filename)
    meta["id"] = meta.get("id", random.randint(1, 100000))
    meta["name"] = filename
    meta["projectId"] =meta.get("projectId", 1)
    meta["created_at"] = datetime.now()
    meta["last_modified"] = datetime.now()
    meta["deleted_at"] = None
    meta["moved"] = 0
    meta["size"] = None
    meta["content_id"] = meta["id"]
    meta["contentType"] = contentType

    ensure_dir(get_metadata_path(project, filename))
    with open(get_metadata_path(project, filename), "wb") as f:
        pickle.dump(meta, f)


def save_file(project, filename, file_object):
    path = get_project_file_path(project, filename)
    ensure_dir(path)
    file_object.save(path)


def get_files_list(project_home):
    return (os.path.relpath(path, project_home) for path in glob(project_home + "/**/*", recursive=True) if os.path.isfile(path))


def hash_file(file_path):
    with open(file_path, "rb") as f:
        m = md5(f.read())
        return m.hexdigest()


def get_poll(project):
    project_home = os.path.join(PROJECTS_DIR, project, "files")
    return {
        "/" + f.replace("\\", "/"): hash_file(os.path.join(project_home, f)) for f in get_files_list(project_home)
    }


def prepare_metadata(project, d):
    if "json" in d.get("contentType", ""):
        d["content"] = open(os.path.join(PROJECTS_DIR, project, "files", d["name"]), "r").read()
    return d


def get_files_descriptors(project):
    project_home = os.path.join(PROJECTS_DIR, project, "files")
    return [
        prepare_metadata(project, get_metadata(project, f)) for f in get_files_list(project_home)
    ]
