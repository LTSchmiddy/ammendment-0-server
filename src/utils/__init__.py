import os
from types import FunctionType
from typing import Union

from colors import color

ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

def mkdir_if_missing(dir_path: str):
    if not os.path.isdir(dir_path):
        # os.mkdir(dir_path)
        os.makedirs(dir_path)



def list_contains(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return True
    return False

def list_get(p_filter, p_list):
    for x in p_list:
        if p_filter(x):
            return x
    return None



def get_dir_tree(current_dir, callback: FunctionType=None, to_ignore: Union[tuple, list]=('__pycache__',)):
    dir_cont = os.listdir(current_dir)

    dir_dict = {
        'path': current_dir,
        'dirs': {},
        'files': {}
    }

    
    for i in dir_cont:
        if i in to_ignore:
            continue

        fullpath = os.path.join(current_dir, i).replace("\\", "/")
        
        if callback is not None:
            result = callback(i, fullpath, current_dir)
            
            if not (result is None or bool(result) is True):
                continue

        if os.path.isfile(fullpath):
            dir_dict['files'][i] = fullpath

        elif os.path.isdir(fullpath):
            dir_dict['dirs'][i] = get_dir_tree(fullpath, callback, to_ignore)


    return dir_dict


def print_color(fg: str, *args, **kwargs):
    p_list = []
    for i in args:
        p_list.append(color(str(i), fg=fg))

    print(*p_list, **kwargs)


def print_error(*args, **kwargs):
    print_color("red", *args, **kwargs)


def print_warning(*args, **kwargs):
    print_color("yellow", *args, **kwargs)


def yn_prompt(msg: str = "", default=None):
    while True:
        result = input(msg).lower()

        if result == "y":
            return True
        if result == "n":
            return False

        if default is not None:
            print_error("Using default...")
            return default

        print_error("Invalid response. Try again...")


def exec_path(path: str):
    if os.name == "nt":
        return path + ".exe"
    return path



from . import anon_func, json_class, std_handler

__all__ = (
    'mkdir_if_missing',
    'list_get', 
    'list_contains', 
    'get_dir_tree',
    "print_color",
    "print_error",
    "print_warning",
    "yn_prompt", 
    'anon_func', 
    'json_class', 
    'std_handler'
)