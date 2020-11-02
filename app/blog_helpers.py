import os
from flask import send_file

_VIEWS_PATH = 'app/templates'
def _set_path(file_name, dir_path_append):
    dir_path = _VIEWS_PATH
    if not dir_path_append is None:
         dir_path = os.path.join(dir_path, dir_path_append)
    path = os.path.join(dir_path, file_name)
    return path

def render_page(file_name, dir_path_append = None):
    path = _set_path(file_name, dir_path_append)
    html = ""
    if file_name.endswith('.png'):
        path = path[path.find('/')+1:]
        html = send_file(path, mimetype='image/png')
    else:
        with open(path) as html_file:
            html = html_file.read()
    return html

def page_exists(file_name, dir_path_append = None):
    path = _set_path(file_name, dir_path_append)
    return os.path.isfile(path)

def get_page_files():
    files = []
    for (path, dn, fn) in os.walk(_VIEWS_PATH):
        for n in fn:
            files.append(n)
    # Next step: Look in SQL Database for descriptions
    return files