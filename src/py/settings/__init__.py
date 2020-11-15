# __all__

import sys
import os
import colorsys
import json

from colors import *
# print(sys.argv[0])



exec_dir, exec_file = os.path.split(os.path.abspath(sys.argv[0]))

exec_dir = exec_dir.replace("\\", "/")
# If we're executing as the source version, the main .py file  is actually found in the `src` subdirectory
# of the project, and `exec_dir` is changed to reflect that. We'll create `exec_file_dir` in case we actually need the
# unmodified path to that script. Obviously, in build mode, these two values will be the same.
exec_file_dir = exec_dir

def is_build_version():
    return exec_file.endswith(".exe")


def is_source_version():
    return exec_file.endswith(".py")


def get_exec_path(path):
    return os.path.join(exec_dir, path)


if is_source_version():
    path_arr = exec_dir.split("/")
    exec_dir = "/".join(path_arr[: len(path_arr) - 1]).replace("/", "\\")

print(f"Is Source: {is_source_version()}")
print(f"Is Build: {is_build_version()}")
print(f"Exec Dir: {exec_dir}")

settings_path = "settings.json"

default_settings = {
    "interface": {
        "app-root": "",
        "pages": {"template-dir": "templates", "static-dir": "static"},
        "view-panes": {
            "template-dir": "templates",
            # 'template-dir': "templates/view_pane_templates",
            "static-dir": "static",
        },
        "api": {"template-dir": "apl_templates", "static-dir": "static"},
        "flask-address": "127.0.0.1",
        "flask-port": 1776,
        "jquery-icon-mode": False,
    },
    "server" : {
        "ssl-context": None
    },
    "database": {
        "db-address": "sqlite:///site-data.db",
        "echo": False
    }
}

current = default_settings.copy()


def load_settings():
    global current
    current = default_settings.copy()

    def recursive_load_list(main: list, loaded: list):
        for i in range(0, max(len(main), len(loaded))):
            # Found in both:
            if i < len(main) and i < len(loaded):
                if isinstance(loaded[i], dict):
                    recursive_load_dict(main[i], loaded[i])
                elif isinstance(loaded[i], list):
                    recursive_load_list(main[i], loaded[i])
                else:
                    main[i] = loaded[i]
            # Found in main only:
            elif i < len(loaded):
                main.append(loaded[i])


    def recursive_load_dict(main: dict, loaded: dict):
        new_update_dict = {}
        for key, value in main.items():
            if not (key in loaded):
                continue
            if isinstance(value, dict):
                recursive_load_dict(value, loaded[key])
            elif isinstance(value, list):
                recursive_load_list(value, loaded[key])
            else:
                new_update_dict[key] = loaded[key]

        main.update(new_update_dict)

    # load preexistent settings file
    if os.path.exists(settings_path) and os.path.isfile(settings_path):
        try:
            imported_settings = json.load(open(settings_path, "r"))
            # current.update(imported_settings)
            recursive_load_dict(current, imported_settings)
        except json.decoder.JSONDecodeError as e:
            print (color(f"CRITICAL ERROR IN LOADING SETTINGS: {e}", fg='red'))
            print (color("Using default settings...", fg='yellow'))

    # settings file not found
    else:
        save_settings()


def save_settings():
    global current
    json.dump(current, open(settings_path, "w"), indent=4)


def validate_settings() -> list:
    import settings.paths as p

    global current
    retVal = []

    return retVal


# load_settings()
from settings import paths
