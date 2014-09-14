# Extended user management

import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from eapptools import model
from eapptools import validation as val

USER_ID_PREFIX_GOOGLE = 'G'

logger = logging.getLogger("user_manager")

class User(model.ModelBase):
	"""Extended user information, linked to the Google identity"""
	
	# Link to the Google user
	google_user = None
	
	# The Google user id
	userName = ndb.StringProperty(required=True)
	firstName = ndb.StringProperty()
	lastName = ndb.StringProperty()
	primaryEmail = ndb.StringProperty()
	createdDate = ndb.DateTimeProperty(auto_now_add = True)
	updatedDate = ndb.DateTimeProperty(auto_now = True)
	
	
	@classmethod
	def parent_key(cls, data_dict = None):
		return ndb.Key(model.BASE_MODEL, "user")
		
	def copy_from_dict(self, data_dict):
		"""Copies the data from a dictionary"""
		
		result = []
		if (data_dict):
			self.userName = val.get_string(data_dict, 'userName', result, mandatory = True)
			self.firstName = val.get_string(data_dict, 'firstName', result)
			self.lastName = val.get_string(data_dict, 'lastName', result)
			self.primaryEmail = val.get_string(data_dict, 'primaryEmail', result)
			
		if len(result) > 0:
			raise va.ValidationError(result)	
			
def current_user(create_user = True):
	"""Gets the current user record from the database"""
	google_user = users.get_current_user()
	
	if not google_user:
		return None
	
	user_key = User.get_key({'id' : USER_ID_PREFIX_GOOGLE + google_user.user_id()})
	user = user_key.get()
	
	if user:
		logger.debug("User %s found", user.key)
	else:
		logger.debug("No user found")
	
	# auto-create user record
	if not user and create_user:
		logger.info("Create new user for Google user ID %s", google_user.user_id())
		user = User.create({
			"id" : USER_ID_PREFIX_GOOGLE + google_user.user_id(),
			"userName" : google_user.nickname()
		})
		user.put()
		
	user.google_user = google_user
	
	return user

	