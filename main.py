#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from util.core import EtherHandler,LoginManager
from util.core import SessionSetup
from util.render import Render
import logging
from amazonproduct import API
from google.appengine.api import memcache
import traceback

class Amazon(EtherHandler):
	def get(self):
		api = API(locale='us',access_key_id="AKIAJNV3URTMY6USU2IA", secret_access_key="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",associate_tag="ethercheckout-20")
		key ="%s" % self.request.get('query')

		cache = memcache.get(key)
		if not cache:
			try:
				# cache = api.item_search('Apparel', ItemPage=1, Condition='All',Availability='Available', Keywords='Shirt')
				cache = api.item_search('Books',Keywords='%s' % self.request.get('query'),Condition='New',Availability='Available')
				objetos = []
				for item in cache:
					# print(dir(item))
					# print(item.ASIN)
					print(item.__dict__)
					if 'DetailPageURL' in item.__dict__:
						self.response.write("<a target=_blank href=%s>%s</a>" % (item.DetailPageURL,item.DetailPageURL))

					self.response.write("<hr>")
					
					self.response.write(item.__dict__)

					self.response.write("<hr>")
					
					objetos.append(item)
				# cache = api.item_search('Toys', Keywords='Rocket')
				

				# memcache.add(key,objetos)

			except:
				dicionario = {'exception': traceback.format_exc()}
				logging.error("Erro ao  renderizar Exception: %s", dicionario['exception'])
				cache = []
		

		# if cache:
		# 	for item in cache:
		# 		print(dir(item))
		# 		if 'DetailPageURL' in item.keys():
		# 			self.response.write(item['DetailPageURL'])
		# 		# ['ASIN', 'DetailPageURL', 'ItemAttributes', 'ItemLinks', 
		# 		# '__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', 
		# 		# '__doc__', '__format__', '__getattr__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '_init', 'addattr', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'clear', 'countchildren', 'descendantpaths', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'sourceline', 'tag', 'tail', 'text', 'values', 'xpath']

		# 		# logging.error(dir(book))
		# 		self.response.write('%s<hr>%s' % (item.ASIN))



class Profile(LoginManager):
	def get(self):
		if self.logged_in:
			self.response.write(self.renderView("home/profile.theme",self.environDict,"ethereum"))
		else:
			d = self.environDict
			d.update({'destination_url':'/profile/'})
			self.response.write(self.renderView("home/login.theme",d,"ethereum"))

class Login(LoginManager):
	def get(self):
		if self.logged_in:
			self.response.write(self.renderView("home/profile.theme",self.environDict,"ethereum"))
		else:
			d = self.environDict
			d.update({'destination_url':'/profile/'})
			self.response.write(self.renderView("home/login.theme",d,"ethereum"))


class Signup(LoginManager):
	def get(self):
		if self.logged_in:
			self.response.write(self.renderView("home/profile.theme",self.environDict,"ethereum"))
		else:
			d = self.environDict
			d.update({'destination_url':'/profile/'})
			self.response.write(self.renderView("home/login.theme",d,"ethereum"))



class CatchAll(EtherHandler):
	def get(self):
		self.response.write(self.renderView("home/index.theme",self.environDict,"ethereum"))

class AmazonSearch(EtherHandler):
	def get(self):
		self.response.write(self.renderView("home/amazon.theme",self.environDict,"ethereum"))

class Pricing(EtherHandler):
	def get(self):
		self.response.write(self.renderView("home/pricing.theme",self.environDict,"ethereum"))


class MainHandler(EtherHandler):
	def get(self):
		self.response.write(self.renderView("home/index.theme",self.environDict,"ethereum"))


app = webapp2.WSGIApplication([
	webapp2.Route('/', MainHandler),
	webapp2.Route('/amazon/',Amazon),
	webapp2.Route('/marketplace/amazon/',AmazonSearch),
	webapp2.Route('/pricing/', handler='main.Pricing', name='pricing'),
	webapp2.Route('/login/', handler='main.Profile', name='login'),
	webapp2.Route('/profile/', handler='main.Profile', name='profile'),
	webapp2.Route('/signup/', handler='main.Profile', name='signup'),
	webapp2.Route('/logout/', handler='util.core.LoginManager:logout', name='logout'),
	webapp2.Route('/auth/<provider>',handler='util.core.LoginManager:_simple_auth', name='auth_login'),
	webapp2.Route('/auth/<provider>/callback',handler='util.core.LoginManager:_auth_callback', name='auth_callback'),
	('/.*', CatchAll)
], config=SessionSetup)