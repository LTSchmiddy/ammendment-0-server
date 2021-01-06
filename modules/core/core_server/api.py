import module_loader
host: module_loader.AZeroModuleHost = None

import os
import sys
import base64
import json

from flask import *
from jinja2 import TemplateNotFound
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from .flask_site import create_app

from utils import print_error
import settings

from . import host

api = Blueprint(
    'api',
    __name__,
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['api']['template-dir'],
    # static_folder=settings['interface']['api']['static-dir']
    root_path=settings.exec_dir,
    template_folder=os.path.join(settings.exec_dir, settings.current['interface']['api']['template-dir']),
    static_folder=os.path.join(settings.exec_dir, settings.current['interface']['api']['static-dir'])
)





# This protocol is designed to keep user interaction with the server well-encrypted,
# Even without HTTPS
@api.route('/', methods=["POST", "GET"])
def index():
    message = request.form['message']
    
    # print(message)
    
    decrypted = host.encryption.decrypt_with_server_key(message)
    
    print(decrypted)
    

    response = host.encryption.encrypt_with_key(decrypted["user_id"].encode('utf-8'), decrypted)
    # print(response)
    return {'response': response}
    # return tuple(response)


@api.route('/show_image')
def show_image():
    # if request.method == "POST":
    path = request.args['path']

    resp = make_response(open(path, 'rb').read())
    if path.endswith('.jpg'):
        resp.content_type = "image/jpeg"
    elif path.endswith('.png'):
        resp.content_type = "image/png"

    return resp