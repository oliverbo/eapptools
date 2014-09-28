import webapp2
import json
import logging
import eapptools
import eapptools.validation as val
from eapptools import model
from google.appengine.api import users

logger = logging.getLogger("resource")

class ResourceDescriptor:
	entity_class = None
	get_permission = eapptools.ACCESS_NONE
	post_permission = eapptools.ACCESS_NONE
	delete_permission = eapptools.ACCESS_NONE
	path_elements = ('id',)
	auto_create = False
	
	def __init__(self, entity_class, 
		get_permission = eapptools.ACCESS_NONE, 
		post_permission = eapptools.ACCESS_NONE, 
		delete_permission = eapptools.ACCESS_NONE,
		path_elements = ('id',),
		auto_create = False):
		
		self.entity_class = entity_class
		self.get_permission = get_permission
		self.post_permission = post_permission
		self.delete_permission = delete_permission
		self.path_elements = path_elements
		self.auto_create = auto_create

class ResourceHandler(webapp2.RequestHandler):
	"""Web request handler for restful resources"""

	def get(self):
		logger.info('API request %s', self.request.path)
		(resource_descriptor, param) = _get_resource_descriptor(self.request.path, 
			self.app.config.get(eapptools.CFG_RESOURCE_MAPPING))
		
		if not resource_descriptor:
			self.response.status = '400 Bad Request'
		else:
			permission = resource_descriptor.get_permission
			if permission == eapptools.ACCESS_NONE or (permission == eapptools.ACCESS_ADMIN and not users.is_current_user_admin()):
				self.response.status = '403 Not Authorized'
			else:
				entity_class = resource_descriptor.entity_class
			
				if len(param) == 0:
					result = entity_class.find_all()
					logger.debug('Result: %s', result)
				else:
					result = entity_class.find(param)
				if not result:
					self.response.status = '404 Not Found'
				else:
					r = eapptools.model.to_json(result)
					logger.debug("Result: %s", r)
					self.response.content_type = "application/json"
					self.response.write(r)
	
	def post(self):
		logger.info("received post request: %s ", self.request.body)
		(resource_descriptor, param) = _get_resource_descriptor(self.request.path, 
			self.app.config.get(eapptools.CFG_RESOURCE_MAPPING))
		if not resource_descriptor:
			self.response.status = '400 Bad Request'
		else:
			permission = resource_descriptor.post_permission
			logger.debug("Permission level %s", permission)
			if permission == eapptools.ACCESS_NONE or (permission == eapptools.ACCESS_ADMIN and not users.is_current_user_admin()):
				logger.warning("Unauthorized POST API access")
				self.response.status = '403 Not Authorized'
			else:
				entity_class = resource_descriptor.entity_class
				data = json.loads(self.request.body)
				# adding URL parameters to data
				data.update(param)
				logger.debug("Data: %s", data)
				try:
					key = entity_class.get_key(data)
					logger.debug("Key found: %s", key)
					entity = key.get()
					logger.debug("Entity found: %s", entity)
					if entity:
						entity.copy_from_dict(data)
						logger.debug("Updating %s", entity)
					elif resource_descriptor.auto_create:
						entity = entity_class.create(data)
						logger.debug("Inserting %s", entity)
					else:
						self.response.status = '400 Bad Request'
					if entity:
						entity.validate()
						key = entity.put()
						self.response.content_type = "application/json"
						if entity.id_field_name() == model.ID_FIELD_NAME:
							self.response.write('{"id" : "%s"}' % key.id())
						else:
							self.response.write('{"key" : "%s"}' % key.urlsafe())
				except val.ValidationError as e:
					self.response.status = '400 Bad Request'
					self.response.content_type = "application/json"
					response_message = ErrorResponse(val.ERR_VALIDATION, e.result).to_json()
					logger.debug("Error message: %s", response_message)
					self.response.write(response_message)
			
	def delete(self):
		logger.info("received delete request: %s ", self.request.body)
		(resource_descriptor, param) = _get_resource_descriptor(self.request.path, 
			self.app.config.get(eapptools.CFG_RESOURCE_MAPPING))
		if not resource_descriptor or not key:
			self.response.status = '400 Bad Request'
		else:
			permission = resource_descriptor.delete_permission
			if permission == eapptools.ACCESS_NONE or (permission == eapptools.ACCESS_ADMIN and not users.is_current_user_admin()):
				self.response.status = '403 Not Authorized'
			else:
				entity_class = resource_descriptor.entity_class
				try:
					entity = entity_class.find(param)
					if entity:						
						entity.delete()
					else:
						self.response.status = '404 Not Found'
				except:
					self.response.status = '400 Bad Request'
					self.response.content_type = "application/json"
					response_message = ErrorResponse(val.ERR_DELETE, e.result).to_json()
					logger.debug("Error message: %s", response_message)
					self.response.write(response_message)
					
def _get_resource_descriptor(path, mapping):
	"""Finds the resource descriptor by splitting the path"""
	path_elements = path.split('/')
	param_index = 0
	param = {}
		
	# Looping through the elements to find a matching handler
	resource_path = ''
	resource_descriptor = None
	logger.debug('found mapping %s', mapping)
	for p in path_elements:
		logger.debug("Element %s", p)		
		if not resource_descriptor:
			resource_path += p
			logger.debug('looking for resource descriptor for %s', resource_path)
			if resource_path in mapping:
				logger.debug("resource descriptor found for %s", resource_path)
				resource_descriptor = mapping[resource_path]
			else:
				resource_path += '/'
		else:
			logger.debug('param %s on position %d', p, param_index)
			if len(resource_descriptor.path_elements) > param_index:
				param[resource_descriptor.path_elements[param_index]] = p
				param_index = param_index + 1
	
	if resource_descriptor:
		logger.info("Resource descriptor found for %s and parameter %s", resource_path, param)
		return (resource_descriptor, param)
	else:
		return (None, None)