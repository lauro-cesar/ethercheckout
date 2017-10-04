__author__ = 'olarva'
__company__ = 'HostCERT'

import logging
import os
import random
import re
from google.appengine.ext import vendor


# appstats_stats_url = '/_ah/stats'
# appstats_RECORD_FRACTION = 1.0

# def webapp_add_wsgi_middleware(app):
#   from google.appengine.ext.appstats import recording
#   app = recording.appstats_wsgi_middleware(app)
#   return app


vendor.add('lib')
os.path.expanduser = lambda path: path