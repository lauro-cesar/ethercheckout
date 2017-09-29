import webapp2
from webapp2_extras import auth, sessions, jinja2


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
	}
}



class BaseHandler(webapp2.RequestHandler):
	



	@webapp2.cached_property
	def getAccountID(self):
		return self.getHostName

	@webapp2.cached_property
	def getHostName(self):
		if 'Host' in self.request.headers:
			return self.request.headers['Host']
		return 'superserver.ethercheckout.io'

	@webapp2.cached_property
	def environDict(self):
		return {
			'accountID':self.getAccountID,
			'hostname':self.getHostName
		}

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



class LoginRequired(BaseHandler):
	def post(self):
		pass

	def get(self):
		pass

	def execute(self):
		pass



class EtherHandler(BaseHandler):
	def post(self):
		pass

	def get(self):
		pass

	def execute(self):
		pass
