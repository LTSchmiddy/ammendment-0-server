import os
import sys
import base64

from flask import *
from .flask_site import app
from jinja2 import TemplateNotFound
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


from settings import current, exec_dir

# private_key = RSA.import_key(open("pkey.pem").read())
private_key =  RSA.import_key(
"""
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAg+wSepQEEgOGYCp9u8fykOjKJm3lhUr0S1QZcSceez7mzTIP
IiokY72svwM8Vn0Fr8Fs79dfp8B4yN9TpMKxBgbz8Qfw7ep7Muq9A8HZZYcUbD5f
gIMBVAalIUwt8G2epS30xuxmPt1Q26c/PkU6NTha1YPaPdb8yKFcu842zDS5Gviv
3JDWlMQm6dE8wkk9DJFHrZYCW1O4kS5Y/wcdpqaf25zgfDXai54xTAh7uz9Cjuls
Wvc3X+zP6YibxDt/itFpxI/L5bRlAfT8vgooL9CTpIqmzNsbw6ik+kK+W+JoZUno
zULZHwtFTrkMeP+660cXvnyLFlvzgQq8mzh9rQIDAQABAoIBAAwdq1jMrU8GOdot
LN0JMRLz/lTnNPQ3/RXKBIgq4pbJISNpXJBztGHgsrPcVTdQRixtJFcmvadHexBf
ymvQYbe+/bp+UzdWmLgFbRSiQhgb/tkuJVFFNuMDtTjIqVNyjeZ3wQpf/cf6RYnW
420RqJXothb0BCA31YGLqFurRccdUT2kq+VUKt573rmjiyRhsiQ9QordxPjQBFNv
Op7u0sSuqcl27zCw6z2ibYrwL2b2JI61U+zQoqLyt71+m5DWehWML52W81372dVb
ZATuU4GUlk1SyCrVJTEQKX98CBGF1NKSGUtIydWOqMndXnx2oHU/9j7jnk2lCYmq
S/9fvXUCgYEA90poK3DZbC5tuCmVGIo1dPjHBmH4IiOyZEfj3TjAD8GioZ3gbPAF
LoV1er9s+LUkxN/m+MweMzV7X1uTkI6yfoh+wvjrYd3Uz7wYIjt/IhCG8urE1RSE
KwCUuksZwodBTIiXV7qs+A+D3YpVG7SOj3l/YF5f/+T+2HjDDwRXaucCgYEAiJF+
Smg55TRUw9X1FHFf7x/aIPc4UPzEMxeXCejWUJAwP7wnLcTAxfHtiyarfUaZ7+5N
UsKAEAzIhBFS3eTD3xwrulPDVjaxGnlm5XgxbtcFlOfUz+hYTOuCuzDnFAH5AfxN
WKitZPAIxd4+PgM253vMwayswvDpyyuA5d+I9EsCgYEAspgPQYhfzix92ypU3oM6
dj8RZf+tN+K1/Iya+XL56qc68CPYKHT0GRQTs1G6vqf8ZR8bbYXlLbCraEP3/8e/
C3lCq0cgn+6Yumqqt1Zmy9BJ1fhNrWICzhe+UgjZEs+iDkb7nkVYlFKINqCoNLki
2GWz44JlLKdSkj4tCZRmGfMCgYA5UWdB73CtJEOXVgtgoxzyjdnNEDWQuCXYk8QO
oqygb4PwnBWNfhCyg5GBX5+GGsWtD8VgQMXi9pqJ44N2IfebgoVP1KwdWSMHy4BG
OyX0MUbkclC9WfUFg6sAycuSeCl8jdogpdrwjFYCRf61pD+89BbCCqkPwHE/lmip
EiK29QKBgAjpufv779bYJQhu4BW09+Qk1zwn0AOTL2HqAJbWhaSrEVuEfQWDVqLm
tBDQO6iKAjbjgsYXWmrQ1zBK/DkKwVdvNNf2081XxCW8vD1vsxnkXkbYWL8kZhtu
Z1Q2P1Fhqu5WTVpdYYpNZ7YXz5l0VGz+0x77qzEleAxL1q/WEeWB
-----END RSA PRIVATE KEY-----
""".strip(" \n\r"))

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
    
    print(f"{message}")
    print(f"{decrypted}")
    
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