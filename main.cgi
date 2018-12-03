#!/home/g/gks2spbru/.local/bin/python3
# -*- coding: UTF-8 -*-

import sys
from wsgiref.handlers import CGIHandler

from app import app

sys.path.insert(0, '/home/g/gks2spbru/.local/lib/python3.7/site-packages')

class ScriptNameStripper(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = ''
        return self.app(environ, start_response)

app = ScriptNameStripper(app)

CGIHandler().run(app)