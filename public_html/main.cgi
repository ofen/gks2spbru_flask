#!/home/g/gks2spbru/.local/bin/python3
# -*- coding: UTF-8 -*-

import sys
from wsgiref.handlers import CGIHandler
from app import app

sys.path.insert(0, '/home/g/gks2spbru/.local/lib/python3.7/site-packages')

CGIHandler().run(app)