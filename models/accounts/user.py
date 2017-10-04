__author__ = 'olarva'
__company__ = 'HostCERT'



from google.appengine.ext import ndb
from util.super import BaseModel,AccountIDModel,DateTimeProperty

from webapp2_extras.appengine.auth.models import User


class UserAccount(User,BaseModel,AccountIDModel):
	homeTown = ndb.StringProperty()
	homeGeoPosition = ndb.GeoPtProperty()
	accessLevel = ndb.StringProperty(default="CUSTOMER") # {'0':'ROOT','1':'COSTUMER','2':'SELLER','3':'EVANGELIST','4':'E-SELLER'}
	userSerial = ndb.StringProperty()
	locale = ndb.StringProperty(default="en_US")
	language = ndb.StringProperty(default="pt_BR")
	email = ndb.StringProperty()
	avatar_url = ndb.StringProperty()
	fullName = ndb.StringProperty()
	contactEmail = ndb.StringProperty()
	contactPhone= ndb.StringProperty()
	supportID = ndb.StringProperty()
	isAdmin = ndb.BooleanProperty(default=False)
	isEmailValid = ndb.BooleanProperty(default=False)
	isCleared = ndb.BooleanProperty(default=True)
	isSeller = ndb.BooleanProperty(default=False)
	isDeveloper = ndb.BooleanProperty(default=False)
	isCustomer = ndb.BooleanProperty(default=False)
	isVerified = ndb.BooleanProperty(default=False)
	country = ndb.StringProperty(default="")
	birthdate = DateTimeProperty(auto_now_add=True)
	city = ndb.StringProperty(default="")
	state = ndb.StringProperty(default="")
	continent = ndb.StringProperty(default="")
	email_provided = ndb.StringProperty()
	counted = ndb.BooleanProperty()
	workgroup = ndb.StringProperty()