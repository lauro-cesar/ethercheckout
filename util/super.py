#-*- encoding: utf-8 -*-
__author__ = 'olarva'
__company__ = 'HostCERT'


from google.appengine.ext import ndb


class DateTimeProperty(ndb.DateTimeProperty):
	def _get_for_dict(self, entity):
		value = super(DateTimeProperty, self)._get_for_dict(entity);
		if value:
			return value.isoformat()
		else:
			return datetime.datetime.today()

class DateProperty(ndb.DateProperty):
	def _get_for_dict(self, entity):
		value = super(DateProperty, self)._get_for_dict(entity);
		if value:
			return value.isoformat()
		else:
			return datetime.datetime.today().date()

class BaseModel(ndb.Model):
	dateCreated = DateTimeProperty(auto_now_add=True)
	dateModified = DateTimeProperty(auto_now=True)
	locale = ndb.StringProperty(default='pt_BR')
	language = ndb.StringProperty(default='pt_BR')


	def getID(self):
		try:
			id = self.key.id()
		except:
			self.put()
			id = self.key.id()
		return id 


	def Create(self):
		self.Save()

	def Update(self):
		self.Save()

	def Save(self):
		self.put()
		self.Commit()

	def Destroy(self):
		return self.key.delete()

	def Commit(self):
		pass

class AccountIDModel(ndb.Model):
	accountID = ndb.StringProperty()