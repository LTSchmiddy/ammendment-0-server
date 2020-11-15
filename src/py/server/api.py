import os
import sys
import base64

from flask import *
from .flask_site import app
from jinja2 import TemplateNotFound
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


from settings import current, exec_dir

private_key = RSA.import_key(open("pkey.pem").read())
cipher_rsa = PKCS1_OAEP.new(private_key)

api = Blueprint(
    'api',
    __name__,
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['api']['template-dir'],
    # static_folder=settings['interface']['api']['static-dir']
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['api']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['api']['static-dir'])
)


# This protocol is designed to keep user interaction with the server well-encrypted,
# Even without HTTPS
@api.route('/', methods=["POST", "GET"])
def index():
    message = request.form['message']

    base64_bytes = message.encode('utf8')
    message_bytes = base64.b64decode(base64_bytes)
    
    decrypted = cipher_rsa.decrypt(message_bytes)
    
    print(f"{message=}")
    print(f"{decrypted=}")
    
    return decrypted




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