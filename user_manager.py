# Extended user management

import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from eapptools import model
from eapptools import validation as val

logger = logging.getLogger("user_manager")

class User(model.ModelBase):
	"""Extended user information, linked to the Google identity"""
	
	# Link to the Google user
	google_user = None
	
	# The Google user id
	uniqueName = ndb.StringProperty()
	firstName = ndb.StringProperty()
	lastName = ndb.StringProperty()
	createdDate = ndb.DateTimeProperty(auto_now_add = True)
	updatedDate = ndb.DateTimeProperty(auto_now = True)
	
	
	@classmethod
	def parent_key(cls):
		return ndb.Key("Base", "user")
		
	def copy_from_dict(self, data_dict):
		"""Copies the data from a dictionary"""
		
		result = []
		if (data_dict):
			self.uniqueName = val.get_string(data_dict, 'uniqueName', result, mandatory = True)
			self.firstName = val.get_string(data_dict, 'firstName', result)
			self.lastName = val.get_string(data_dict, 'lastName', result)
			
		if len(result) > 0:
			raise va.ValidationError(result)
			
def current_user(create_user = True):
	"""Gets the current user record from the database"""
	google_user = users.get_current_user()
	
	if not google_user:
		return None
	
	user = User.find(google_user.user_id())
	
	# auto-create user record
	if not user and create_user:
		logger.info("Create new user for %s", google_user.user_id())
		user = User.create({"uniqueName" : google_user.user_id()})
		user.put()
		
	user.google_user = google_user
	
	return user

	