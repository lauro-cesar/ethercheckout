import webapp2
from webapp2_extras import auth, sessions, jinja2


import json
import os
import re
import time
import urllib
import traceback
from google.appengine.api import app_identity,urlfetch,memcache
import httplib2
import base64
import logging


import webob.multidict

from webapp2_extras import auth, sessions, jinja2
from webapp2_extras import sessions_memcache

from oauth2client.client import GoogleCredentials
from util.environ import _IDENTITY_ENDPOINT,_FIREBASE_SCOPES,_FIREBASE_URL,ignore,marketPrefix

import util.secrets


from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler
from util.render import Render

DEFAULT_AVATAR_URL = '/img/missing-avatar.png'
FACEBOOK_AVATAR_URL = 'https://graph.facebook.com/{0}/picture?type=large'
FOURSQUARE_USER_LINK = 'http://foursquare.com/user/{0}'


SessionSetup = {
	'webapp2_extras.sessions': {
		'secret_key': '7091820D-0B0C-4DA0-823B-2454272F4D3B',
		'cookie_name': 'etherCheckout-2017',
		'cookie_args': {
			'max_age': 60 * 60 * 24 * 365,
			'domain': None,
			'path': '/',
			'secure': False,	
			'httponly': False,
		}
	},
	'webapp2_extras.auth': {
		'user_model': 'models.accounts.user.UserAccount',
		'user_attributes': []
	}
}


class BaseHandler(webapp2.RequestHandler,Render):
	def head(self, *args):
		pass

	@webapp2.cached_property
	def getAccountID(self):
		return self.getHostName

	@webapp2.cached_property
	def getHostName(self):
		if 'Host' in self.request.headers:
			return self.request.headers['Host']
		return 'www.ethercheckout.io'

	@webapp2.cached_property
	def loginOptions(self):
		return [
			{
			'path':'/auth/googleplus',
			'label':'Google+',
			'icon':'google',
			'class':'google plus'
			},{
			'path':'/auth/live',
			'label':'Windows live',
			'icon':'windows',
			'class':'windows'
			},
			{
			'path':'/auth/twitter',
			'label':'Twitter',
			'icon':'twitter',
			'class':'twitter'
			},
			{
			'path':'/auth/facebook',
			'label':'Facebook',
			'icon':'facebook',
			'class':'facebook'
			}

			]
	@webapp2.cached_property
	def environDict(self):
		return {
			'accountID':self.getAccountID,
			'hostname':self.getHostName,
			'fireToken':self.fireToken,
			'etherCurrencies':self.getEtherCurrencies,
			'etherMarkets':self.getEtherMarkets,
			'marketPrefix':marketPrefix,
			'url_for': self.uri_for,
			'logged_in': self.logged_in,
			'flashes': self.session.get_flashes(),
			'user':self.current_user,
			'session':self.session,
			'loginOptions':self.loginOptions
		}

	@webapp2.cached_property
	def getHttp(self):
		http = httplib2.Http()
		creds = GoogleCredentials.get_application_default().create_scoped(_FIREBASE_SCOPES)
		creds.authorize(http)
		return http


	def updateMarket(self,dicionario):
		# http = httplib2.Http()
		# creds = GoogleCredentials.get_application_default().create_scoped(_FIREBASE_SCOPES)
		# creds.authorize(http)
		logging.error("Atualizando mercados: %s" % dicionario['MarketName'])
		url = '{}/market/{}.json'.format(_FIREBASE_URL,dicionario['MarketName'])
		# logging.error(url)

		pacote = json.dumps(dicionario)
		resposta = self.getHttp.request(url, 'PATCH', body=pacote)

		# logging.error(resposta)
		# http.request(url, 'PATCH', body=json.dumps(dicionario))


	def getUrlContent(self,url):
		pass


	def getCurrencyMarket(self,marketName):
		# logging.error("Getting market: %s" % marketName)
		key="bittrex_market"

		market = memcache.get(key)
		if not market:	
			market = []
			url = "https://bittrex.com/api/v1.1/public/getmarketsummary?market=%s" % marketName
			try:
				result = urlfetch.fetch(validate_certificate=True,url=url,method=urlfetch.GET,headers={'Accept': 'application/json'})
				if result.status_code == 200:
					j = json.loads(result.content)
					market=j['result']
					memcache.add(key,market,60)
				else:
					market = []
			except:
				market = []

		return market


	@webapp2.cached_property
	def getAllCurrencies(self):
		key="bittrex_currencies"

		currencies = memcache.get(key)

		if not currencies:
			currencies=[]
			url = "https://bittrex.com/api/v1.1/public/getcurrencies"
			try:
				result = urlfetch.fetch(validate_certificate=True,url=url,method=urlfetch.GET,headers={'Accept': 'application/json'})
				if result.status_code == 200:
					j = json.loads(result.content)
					currencies = j['result']
					memcache.add(key,currencies)
				else:
					currencies=[]
			except:
				currencies=[]
		return currencies

	@webapp2.cached_property
	def getAllMarkets(self):
		key="bittrex_all_markets"
		all_markets = memcache.get(key)
		if not all_markets:
			all_markets=[]
			try:
				url="https://bittrex.com/api/v1.1/public/getmarkets"
				result = urlfetch.fetch(validate_certificate=True,url=url,method=urlfetch.GET,headers={'Accept': 'application/json'})
				if result.status_code == 200:
					j = json.loads(result.content)
					# logging.error(j['result'])
					all_markets = j['result']
				else:
					all_markets = []

			except:
				all_markets = []

		return all_markets

	@webapp2.cached_property
	def getEtherMarkets(self):
		moedas=['ETH','ETH_CONTRACT']
		mercados = self.getAllMarkets
		lista = []

		for m in mercados:
			if m['BaseCurrency'] in moedas:
				lista.append(m)
		return lista

	@webapp2.cached_property
	def getEtherCurrencies(self):
		key = "etherCurrencies"
		moedas =['ETH','ETH_CONTRACT']
		lista = memcache.get(key)

		if not lista:
			lista=[]
			dicionario={}
			for c in self.getAllCurrencies:
				if c['CoinType'] in moedas:
					key = c['Currency']
					# lista[key]=c
					lista.append({key:c})
			if lista:
				memcache.add(key,lista,3600*24)

		return lista




	@webapp2.cached_property
	def fireToken(self):
		client_email = app_identity.get_service_account_name()
		# logging.error(client_email)
		now = int(time.time())
		iat = now
		exp = now + ( 60 * 59 )
		# logging.error(now)
		# logging.error(exp)

		payload = base64.b64encode(json.dumps({
		'iss': client_email,
		'sub': client_email,
		'aud': _IDENTITY_ENDPOINT,
		'uid': self.getAccountID,  
		'iat': now,
		'exp': exp,
		}))

		header = base64.b64encode(json.dumps({'typ': 'JWT', 'alg': 'RS256'}))
		to_sign = '{}.{}'.format(header, payload)
		return '{}.{}'.format(to_sign, base64.b64encode(app_identity.sign_blob(to_sign)[1]))


	@webapp2.cached_property
	def jinja2(self):
		return jinja2.get_jinja2(app=self.app)

	@webapp2.cached_property
	def session(self):
		return self.session_store.get_session()

	@webapp2.cached_property
	def auth(self):
		return auth.get_auth()

	@webapp2.cached_property
	def current_user(self):
		user_dict = self.auth.get_user_by_session()
		if user_dict:
			return self.auth.store.user_model.get_by_id(user_dict['user_id'])
		else:
			return {}

	@webapp2.cached_property
	def logged_in(self):
		return self.auth.get_user_by_session() is not None


	def dispatch(self):
		self.session_store = sessions.get_store(request=self.request)
		self.viewSize="large"
		
		# if 'Host' in self.request.headers:
		# 	self.hostname = self.request.headers['Host']


		# if self.request.get('viewSize'):
		# 	self.session['viewSize']=self.request.get('viewSize')


		# if not self.session.get('viewSize'):
		# 	if isMedium.search(self.request.headers['User-Agent']):
		# 		self.session['viewSize']='medium'
		# 		# logging.debug("Salvando como Medium")
		# 	elif isSmall.search(self.request.headers['User-Agent']):
		# 		self.session['viewSize']='small'
		# 		# logging.debug("Salvando como small")
		# 	else:
		# 		# logging.debug("Salvando como Large")
		# 		self.session['viewSize']='large'


		# if self.session.get('viewSize'):
		# 	self.viewSize=self.session.get('viewSize')
		# else:
		# 	self.viewSize="large"



		try:
			webapp2.RequestHandler.dispatch(self)
		except:
			dicionario = {'exception': traceback.format_exc()}
			logging.error("Erro ao  renderizar Exception: %s", dicionario['exception'])
			self.error(500)
			return
		finally:
			self.session_store.save_sessions(self.response)


class LoginManager(BaseHandler, SimpleAuthHandler):
	OAUTH2_CSRF_STATE = True

	USER_ATTRS = {
	'facebook': {
	'id': lambda id: ('avatar_url', FACEBOOK_AVATAR_URL.format(id)),
	'name': 'name',
	'link': 'link'
	},
	'google': {
	'picture': 'avatar_url',
	'name': 'name',
	'profile': 'link'
	},
	'googleplus': {
	'image': lambda img: ('avatar_url', img.get('url', DEFAULT_AVATAR_URL)),
	'displayName': 'name',
	'url': 'link'
	},
	'windows_live': {
	'avatar_url': 'avatar_url',
	'name': 'name',
	'link': 'link'
	},
	'twitter': {
	'profile_image_url': 'avatar_url',
	'screen_name': 'name',
	'link': 'link'
	},
	'linkedin': {
	'picture-url': 'avatar_url',
	'first-name': 'name',
	'public-profile-url': 'link'
	},
	'linkedin2': {
	'picture-url': 'avatar_url',
	'first-name': 'name',
	'public-profile-url': 'link'
	},
	'foursquare': {
	'photo': lambda photo: ('avatar_url', photo.get('prefix') + '100x100'\
							  + photo.get('suffix')),
	'firstName': 'firstName',
	'lastName': 'lastName',
	'contact': lambda contact: ('email', contact.get('email')),
	'id': lambda id: ('link', FOURSQUARE_USER_LINK.format(id))
	},
	'openid': {
	'id': lambda id: ('avatar_url', DEFAULT_AVATAR_URL),
	'nickname': 'name',
	'email': 'link'
	}
	}

	def _on_signin(self, data, auth_info, provider, extra=None):
		auth_id = '%s:%s' % (provider, data['id'])
		user = self.auth.store.user_model.get_by_auth_id(auth_id)
		_attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])
		destination_url = '/profile/'
		if user:
			user.populate(**_attrs)
			user.put()
			self.auth.set_session(self.auth.store.user_to_dict(user))
		else:	
			if self.logged_in:
				user = self.current_user
				user.populate(**_attrs)
				user.add_auth_id(auth_id)

			else:
				ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
				if ok:
					self.auth.set_session(self.auth.store.user_to_dict(user))

					self.session.add_flash(auth_info, 'auth_info')
					self.session.add_flash({'extra': extra}, 'extra')

					
					if extra is not None:
						params = webob.multidict.MultiDict(extra)
						destination_url = str(params.get('destination_url', '/profile'))
		
		return self.redirect(destination_url)

	def logout(self):
		self.auth.unset_session()
		self.redirect('/')

	def handle_exception(self, exception, debug):
		d = self.environDict
		d.update( {'exception': exception})
		logging.error(debug)
		logging.error(exception)
		self.response.write(self.renderView("home/error.theme",d,"ethereum"))
		

	def _callback_uri_for(self, provider):
		return self.uri_for('auth_callback', provider=provider, _full=True)

	def _get_consumer_info_for(self, provider):
		return util.secrets.AUTH_CONFIG[provider]

	def _get_optional_params_for(self, provider):
		return util.secrets.AUTH_OPTIONAL_PARAMS.get(provider)
		
	def _to_user_model_attrs(self, data, attrs_map):
		user_attrs = {}
		for k, v in attrs_map.iteritems():
			attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
			user_attrs.setdefault(*attr)
		return user_attrs








class EtherHandler(BaseHandler):
	def post(self):
		pass

	def get(self):
		pass

	def execute(self):
		pass
