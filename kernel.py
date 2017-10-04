#-*- encoding: utf-8 -*-
__author__ = 'olarva'
__company__ = 'HostCERT'

import webapp2
from webapp2_extras import routes
import logging
import json
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import db
import traceback
import datetime
from google.appengine.api import taskqueue
import uuid
from jinja2 import Template
from jinja2 import Markup



from util.core import EtherHandler
from util.core import SessionSetup
from util.render import Render

from util.environ import ignore
from util.environ import _IDENTITY_ENDPOINT,_FIREBASE_SCOPES,_FIREBASE_URL,ignore,marketPrefix

class UpdateMarket(EtherHandler):
	def get(self):
		# self.response.write(self.getAllCurrencies)
		taskqueue.add(queue_name="MarketManager",url='/kernel/update/market/')
		self.response.write("Atualizando mercados")

	def post(self):
		offset=0
		limit=1
		lap=1
		if self.request.get('limit'):
			limit=int(self.request.get('limit'))
		
		if self.request.get('offset'):
			offset=int(self.request.get('offset'))
		
		if 'lap' in self.request.params:
			lap = lap + int(self.request.get('lap'))

		mercados = self.getEtherMarkets[offset:(offset+limit)]
		for moeda in mercados:
			dicionario={}
			logging.error(moeda)

			dicionario.update(moeda)
				
			market = self.getCurrencyMarket(dicionario['MarketName'].upper())
			if market:
				dicionario.update(market[0])
				self.updateMarket(dicionario)
	

			# logging.error(moeda[currency])
			# self.response.write("<hr>")
		if mercados:
			taskqueue.add(queue_name="MarketManager",url='/kernel/update/market/',params={'offset':(limit+offset),'limit':limit,'lap':lap})



app = webapp2.WSGIApplication([
	routes.PathPrefixRoute('/kernel',[
	webapp2.Route('/update/market/', UpdateMarket),
])], config=SessionSetup)