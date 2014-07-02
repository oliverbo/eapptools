from google.appengine.ext import ndb

class ModelBase(ndb.Model):
	"""Base class for NDB entity classes"""
	model_name = "BASE"
	uniqueName = ndb.StringProperty()
	displayName = ndb.StringProperty()
	
	def validate(self):
		pass

	def copy_data_and_validate(self, data_dict):
		pass