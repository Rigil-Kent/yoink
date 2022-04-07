import atexit
import click
import os
import time
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Role, ComicMeta
from yoink.config import config
from yoink.comic import Comic


def ping(url: str):
    ''' check url for connection status'''
    return requests.get(url).status_code


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_ctx(): return dict(db=db, User=User, Role=Role, ComicMeta=ComicMeta)

@app.context_processor
def inject_status_code():
    return dict(status_code=ping('http://readallcomics.com'))

@app.cli.command()
def test():
    ''' run unit tests '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
