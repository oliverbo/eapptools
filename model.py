import logging
import musicdb
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
	def find(cls, key):
		"""Returns a single enitity identified with the key or None if it cannot be found"""
		query = cls.query(cls.uniqueName == key)
		entities = query.fetch(1)
		logger.info('Found entity for key %s: %s', key, entities)
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
		enities = cls.findAll()
		for entity in entities:
			keys.append(venue.key)			
		logger.info("deleting %s", keys)
		ndb.delete_multi(keys)
		
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
			
def to_json(obj):  
	"""Generic JSON converter that handles also arrays of NDB entities"""  
	return json.dumps(obj, default = lambda o: o.to_dict())

	