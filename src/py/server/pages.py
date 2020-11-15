import os
import sys

from flask import *
from .flask_site import app
from jinja2 import TemplateNotFound

from settings import current, exec_dir

import db
from db.tables import *

# print(os.path.join(exec_dir, current['interface']['pages']['template-dir']))
# print(os.path.join(exec_dir, current['interface']['pages']['static-dir']))

pages = Blueprint(
    'pages',
    __name__,
    root_path=exec_dir,
    template_folder=os.path.join(exec_dir, current['interface']['pages']['template-dir']),
    static_folder=os.path.join(exec_dir, current['interface']['pages']['static-dir'])
    # root_path=os.getcwd(),
    # template_folder=settings['interface']['pages']['template-dir'],
    # static_folder=settings['interface']['pages']['static-dir']
)



@pages.route('/')
def index():
    return "Hello Alex"




