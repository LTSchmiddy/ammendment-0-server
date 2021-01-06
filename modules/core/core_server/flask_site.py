from . import host

import os
import textwrap

from flask import Flask, send_from_directory
import settings
from logging.config import dictConfig

import markdown2
from utils import anon_func
import sqlalchemy

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        # 'stream': 'ext://flask.logging.wsgi_errors_stream',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app():
    app = Flask(__name__, root_path=os.getcwd())
    app.jinja_options['extensions'].append('jinja2.ext.do')

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    # import interface_flask
    from .api import api


    @app.context_processor
    def jinja2_values():

        return dict(
            settings=settings,
            int=int,
            str=str,
            list=list,
            tuple=tuple,
            type=type,
            len=len,
            dir=dir,
            getattr=getattr,
            hasattr=hasattr,
            isinstance=isinstance,
            exec=exec,
            eval=eval,
            filter=filter,
            ordinal=lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4]),
            md=markdown2.markdown,
            db=db,
            sqltypes=sqlalchemy.sql.sqltypes,
            textwrap=textwrap,
            af=anon_func
        )

    # Page endpoints:
    @app.route('/blank')
    def blank():
        return ""
    
    
    # app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api/')
    
    return app
