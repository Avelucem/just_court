from __future__ import absolute_import
import os
from flask import Flask


dbcase = os.path.abspath('dbcase')
DOWNLOAD = os.path.abspath('download')
app = Flask(__name__, static_folder='static')
app.secret_key = 'super secret key'
app.config['dbcase'] = dbcase
app.config['DOWNLOAD'] = DOWNLOAD


import court_parce.views
