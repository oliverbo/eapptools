import logging
import musicdb
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
		return None
	
	@classmethod	
	def delete_all(cls):
		"""Deletes all entities"""
		keys = []
		enities = cls.findAll()
		for entity in entities:
			keys.append(venue.key)			
		logger.info("deleting %s", keys)
		ndb.delete_multi(keys)
	
	def validate(self):
		"""Validates a data object"""
		pass

	