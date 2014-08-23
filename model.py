import logging
import json
from google.appengine.ext import ndb

logger = logging.getLogger("model_base")

MAXDATA = 50

class ModelBase(ndb.Model):
	"""Base class for NDB entity classes"""
	model_name = "BASE"
	uniqueName = ndb.StringProperty()
	
	@classmethod
	def parent_key(cls):
		"""Returns the parent key - by default the base key"""
		return ndb.Key('Base')
	
	@classmethod
	def find_all(cls):
		"""Queries all entities"""
		query = cls.query(ancestor=cls.parent_key())
		return query.fetch(MAXDATA)
	
	@classmethod
	def find(cls, uniqueName):
		"""Returns a single entity identified with the key or None if it cannot be found"""
		query = cls.query(cls.uniqueName == uniqueName)
		entities = query.fetch(1)
		logger.info('Found entity for key %s: %s', uniqueName, entities)
		if (len(entities) == 0):
			return None
		else:
			return entities[0]
			
	@classmethod
	def create(cls, data_dict):
		"""Creates a new entity from a data object"""
		entity = cls(parent = cls.parent_key())
		entity.copy_from_dict(data_dict)
		return entity
	
	@classmethod	
	def delete_all(cls):
		"""Deletes all entities"""
		keys = []
		entities = cls.find_all()
		for entity in entities:
			keys.append(entity.key)			
		logger.info("deleting %s", keys)
		ndb.delete_multi(keys)
		
	@classmethod
	def export_as_json(cls):
		"""Exports all entities as JSON"""
		entities = cls.find_all()
		return to_json(entities)
		
	@classmethod
	def import_from_json(cls, json_data):
		"""imports records from a list of json-formatted objects. All objects are validated"""
		# convert data to venues
		data_list = json.loads(json_data)
		for data_dict in data_list:
			logger.debug("JSON object: %s", data_dict)
			venue = cls.create(data_dict)
			venue.validate()
			venue.put()
		
	def delete(self):
		"""Deletes itself from storage"""
		self.key.delete()
		
	def copy_from_dict(self, data_dict):
		"""Copies the data from a dictionary into the entity. This can result in a ValidationError,
			if the data is not successfully converted"""
		pass
		
	def to_json(self):
		"""Converts the entity to JSON"""
		return to_json(self)
	
	def validate(self):
		"""Validates a data object and results in a ValidationError is the data is invalid"""
		pass

# General utility methods
			
def to_json(obj):  
	"""Generic JSON converter that handles also arrays of NDB entities"""  
	return json.dumps(obj, default = lambda o: o.to_dict())

	