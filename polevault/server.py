# -*- coding: utf-8 -*-

""" Flask app for the graphical user interface.
"""

from __future__ import print_function, division, unicode_literals

import threading
import socket
import time
import sys
import os

from base64 import urlsafe_b64encode

try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

import logging

try:
    import webview
    PYWEBVIEW_AVAILABLE = True
except:
    PYWEBVIEW_AVAILABLE = False

try:
    from flask import Flask, Blueprint, url_for, render_template, jsonify, request, make_response
    app_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'app')
    static_path = os.path.join(app_path, 'static')
    server = Blueprint('polevault', __name__, static_folder=static_path, template_folder=app_path)
    FLASK_AVAILABLE = True
except:
    FLASK_AVAILABLE = False


# import webbrowser


cancel_heavy_stuff_flag = False


@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@server.route("/")
def landing():
    """
    Render index.html. Initialization is performed asynchronously in initialize() function
    """
    return render_template("index.html")


@server.route("/choose/path")
def choose_path():
    """
    Invoke a folder selection dialog here
    :return:
    """
    current_directory = os.getcwd()
    dirs = webview.create_file_dialog(webview.FOLDER_DIALOG,
                                      directory=current_directory)
    if dirs and len(dirs) > 0:
        directory = dirs[0]
        if isinstance(directory, bytes):
            directory = directory.decode("utf-8")
        if directory.startswith(current_directory + os.path.sep):
            directory = directory[len(current_directory) + len(os.path.sep):]

        response = {"message": directory}
    else:
        response = {"message": "cancel"}

    return jsonify(response)


@server.route("/fullscreen")
def fullscreen():
    webview.toggle_fullscreen()
    return jsonify({})


# @server.route("/open-url", methods=["POST"])
# def open_url():
#     url = request.json["url"]
#     webbrowser.open_new_tab(url)
#     return jsonify({})


@server.route("/python_version")
def python_version():
    return jsonify({
        'message': 'Hello from Python {0}'.format(sys.version)
    })


@server.route("/heavy_stuff/do")
def do_stuff():
    time.sleep(0.1)  # sleep to prevent from the ui thread from freezing for a moment
    now = time.time()
    global cancel_heavy_stuff_flag
    cancel_heavy_stuff_flag = False
    response = {
        'message': 'starting stuff'
    }
    for i in range(0, 200000):
        _ = urlsafe_b64encode(os.urandom(80)).decode('utf-8')
        if cancel_heavy_stuff_flag:
            response = {'message': 'Operation cancelled'}
            break
    else:
        then = time.time()
        response = {
            'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
        }

    return jsonify(response)


@server.route("/heavy_stuff/cancel")
def cancel_stuff():
    time.sleep(0.1)
    global cancel_heavy_stuff_flag
    cancel_heavy_stuff_flag = True
    response = {
        'message': 'canceling stuff'
    }
    return jsonify(response)


@server.route("/close_down")
def close_down():
    response = {
        'message': 'closing'
    }
    webview.destroy_window()
    os._exit(0)

    return jsonify(response)


def run_server(port, prefix):
    app = Flask(__name__)
    app.register_blueprint(server, url_prefix=prefix)

    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # disable caching
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.ERROR)
    logger.disabled = True
    app.logger.disabled = True

    so = sys.stdout
    se = sys.stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    app.run(host="127.0.0.1", port=port, threaded=True)
    sys.stdout = so
    sys.stderr = se


def url_ok(host, port, prefix):
    try:
        conn = HTTPConnection(host, port)
        conn.request("GET", prefix)
        r = conn.getresponse()
        return r.status == 200
    except:
        return False


def find_free_port(start=5000, end=5999):
    found = False
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                found = True
        if found:
            return port
    return 0


def gui():
    port = find_free_port()

    if port > 0 and PYWEBVIEW_AVAILABLE and FLASK_AVAILABLE:
        prefix = '/' + urlsafe_b64encode(os.urandom(33)).decode('utf8').rstrip('=') + '/'

        t = threading.Thread(target=run_server, args=(port, prefix))
        t.daemon = True
        t.start()

        # print("http://127.0.0.1:{}{}".format(port, prefix))

        while not url_ok('127.0.0.1', port, prefix):
            time.sleep(0.1)

        webview.create_window('Pole Vault',
                              "http://127.0.0.1:{}{}".format(port, prefix),
                              confirm_quit=True,
        )
    else:
        if not FLASK_AVAILABLE:
            print('''
   You must install the flask package in order to
use the graphical user interface:

     pip install flask

''')
        if not PYWEBVIEW_AVAILABLE:
            print('''
   You must install the pywebview package in order to
use the graphical user interface:

     pip install pywebview

''')
        print('''
   For help about using polevault from the CLI please type:

     polevault --help
''')
        exit(3)


if __name__ == "__main__":
    port = find_free_port()

    if port > 0 and PYWEBVIEW_AVAILABLE and FLASK_AVAILABLE:
        prefix = '/prefix/'

        print("http://127.0.0.1:{}{}".format(port, prefix))

        run_server(port, prefix)
