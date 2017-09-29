#-*- encoding: utf-8 -*-
from util.environ import STATIC_TEMPLATES
import logging

from slimmer import html_slimmer, xhtml_slimmer,css_slimmer

from google.appengine.api import urlfetch,memcache
import traceback
import re



class Render():
	def posProcess(self,renderResult):
		html = html_slimmer(renderResult)
		return html
		
	def renderViewFromString(self,template="<demo></demo>",dicionario={},namespace=None):
		t = STATIC_TEMPLATES.from_string(template)
		return t.render(dicionario)
		
	def renderViewFromStringSlim(self,template="<demo></demo>",dicionario={},namespace=None):
		t = STATIC_TEMPLATES.from_string(template)
		return self.posProcess(t.render(dicionario))
		

	def renderView(self,templatePath,dicionario,namespace=None):
		t = STATIC_TEMPLATES.get_template(templatePath)
		return self.posProcess(t.render(dicionario))