import logging
import json
import datetime
from google.appengine.ext import ndb

logger = logging.getLogger("model_base")

BASE_MODEL = 'BASE'
MAXDATA = 50

ID_FIELD_NAME = 'id'
KEY_FIELD_NAME = 'key'

class ModelBase(ndb.Model):
	"""Base class for NDB entity classes"""
	
	@classmethod
	def parent_key(cls, data_dict = None):
		"""Returns the parent key - by default the base key"""
		return ndb.Key(BASE_MODEL, cls.__name__)
		#raise RuntimeError('parent_key is not defined in sub_class')
				
	@classmethod
	def get_key(cls, data_dict):
		"""Returns the key from either an id or a URL-safe key"""
		if KEY_FIELD_NAME in data_dict:
			return ndb.Key(urlsafe = data_dict[KEY_FIELD_NAME])
		elif ID_FIELD_NAME in data_dict:
			return ndb.Key(parent = cls.parent_key(data_dict), flat=(cls, data_dict[ID_FIELD_NAME]))
		else:
			return None		
			
	@classmethod
	def find_all(cls, data_dict = None):
		"""Queries all entities"""
		query = cls.query(ancestor=cls.parent_key(data_dict))
		return query.fetch(MAXDATA)
	
	@classmethod
	def find(cls, data_dict):
		"""Returns a single entity by either id with parent information or the full key"""
		key = cls.get_key(data_dict)
		
		if not key:
			raise RuntimeError('no id or key element in data')
		return key.get()
			
	@classmethod
	def create(cls, data_dict):
		"""Creates a new entity from a data object. If the dict has a field 'id' it is used as the id in the entities key"""		
		if 'id' in data_dict:
			new_key = ndb.Key(parent = cls.parent_key(data_dict), flat = (cls, data_dict[ID_FIELD_NAME]))
			entity = cls(key=new_key)
		else:
			entity = cls(parent = cls.parent_key(data_dict))
			
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
	
	@staticmethod		
	def id_field_name():
		"""Determines if an entity is identified by ID and parent or the full key"""
		return ID_FIELD_NAME
		
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
	return json.dumps(obj, default=_ndb_json_encoder)
	
def _ndb_json_encoder(obj):
	if isinstance(obj, ModelBase):
		dict = obj.to_dict()
		if obj.id_field_name() == KEY_FIELD_NAME:
			dict[KEY_FIELD_NAME] = obj.key.urlsafe()
		elif obj.id_field_name() == ID_FIELD_NAME:
			dict[ID_FIELD_NAME] = obj.key.id()
		else:
			raise RuntimeError('Invalid id field name %s' % obj.id_field_name())
		return dict
	elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
		return obj.isoformat()
	else:
		return obj.__dict__
	