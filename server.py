from flask import Flask, request, jsonify, make_response, current_app, render_template, url_for, redirect, send_from_directory, Response
import logging
import time
import copy
import json
import os
from datetime import timedelta

__author__ = "Zack Scholl"
__copyright__ = "Copyright 2015, FIND"
__credits__ = ["Zack Scholl", "Stefan Safranek"]
__license__ = "MIT"
__version__ = "0.14"
__maintainer__ = "Zack Scholl"
__email__ = "zack.scholl@gmail.com"
__status__ = "Development"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()])
# Patch because basestring doesn't work for crossdomain()
# https://github.com/oxplot/fysom/issues/1
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """ Decorator for the HTTP access control

    From http://flask.pocoo.org/snippets/56/

    Cross-site HTTP requests are HTTP requests for resources from a different domain 
    than the domain of the resource making the request. For instance, a resource loaded from 
    Domain A makes a request for a resource on Domain B. The way this is implemented in 
    modern browsers is by using HTTP Access Control headers: Documentation on developer.mozilla.org.
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route("/")
def landing():
    return render_template('index.html')

@app.route("/img", methods=['GET'])
def imageserve():
    os.system('cp ./static/new.jpg ./static/test.jpg')
    img_size = os.path.getsize('./static/test.jpg')
    new = False
    if img_size > 100000:
        os.system('cp ./static/test.jpg ./static/image_stream.jpg')
        new = True
    payload = {'src':'/static/image_stream.jpg','time':time.time(),'newimage':new}
    return jsonify(result=payload)
    
if __name__ == "__main__":
    """Main app

    Uses the Flask internals
    """
    app.run(host='0.0.0.0', port=3000)
    # app.run()