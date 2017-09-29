#-*- coding: utf- 8-*- 
__author__ = 'olarva'
__company__ = 'HostCERT'
#User: olarva
#Date: 1/4/15
#Time: 3:07 AM

import logging
import os
import jinja2
import traceback
import webapp2
import json
from jinja2 import BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime
from jinja2 import Template
from jinja2 import Markup
import lxml
from lxml.html.clean import Cleaner
import re
import base64
from decimal import *
from google.appengine.api import urlfetch
import cgi
import hashlib
from google.appengine.api import taskqueue
from google.appengine.api import memcache

from jinja2 import Undefined


themeFiles=['.omni','.theme']
macroFiles=['.macro']
localeFiles=['.locale']
themeDefaultVersion=1.0
import lxml
from lxml.html.clean import Cleaner

isSmall=re.compile('Mobi*',re.IGNORECASE)
isMedium=re.compile('iPad|IPad|Android + Chrome/[.0-9]* (?!Mobile)')



enviroments =[]

STATIC_TEMPLATES = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


enviroments.append(STATIC_TEMPLATES)


