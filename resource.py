import webapp2
import json
import logging
import eapptools
import eapptools.validation as val
from google.appengine.api import users

logger = logging.getLogger("resource")

class ResourceDescriptor:
	entity_class = None
	get_permission = eapptools.ACCESS_NONE
	post_permission = eapptools.ACCESS_NONE
	delete_permission = eapptools.ACCESS_NONE
	
	def __init__(self, entity_class, get_permission = eapptools.ACCESS_NONE, 
		post_permission = eapptools.ACCESS_NONE, delete_permission = eapptools.ACCESS_NONE):
		self.entity_class = entity_class
		self.get_permission = get_permission
		self.post_permission = post_permission
		self.delete_permission = delete_permission	

class ResourceHandler(webapp2.RequestHandler):
	"""Web request handler for restful resources"""
	
	def _get_resource_descriptor(self, path):
		path_elements = self.request.path.split('/')
		
		# Looping through the elements to find a matching handler
		resource_path = ''
		key = None
		resource_descriptor = None
		mapping = self.app.config.get(eapptools.CFG_RESOURCE_MAPPING)
		logger.debug('found mapping %s', mapping)
		for p in path_elements:
			logger.debug("Element %s", p)		
			if not resource_descriptor:
				resource_path += p
				logger.debug('looking for resource descriptor for %s', resource_path)
				if resource_path in mapping:
					logger.debug("resource descriptor found for %s", resource_path)
					resource_descriptor = mapping[resource_path]
					key = ''
				else:
					resource_path += '/'
			elif key == '':
				key += p
				logger.debug('key %s', key)
			else:
				key += '/' + p
		
		if resource_descriptor:
			logger.info("Resource descriptor found for %s and key '%s'", resource_path, key)
			return (resource_descriptor, key)
		else:
			return (None, None)

	def get(self):
		logger.info('API request %s', self.request.path)
		(resource_descriptor, key) = self._get_resource_descriptor(self.request.path)
		
		if not resource_descriptor:
			self.response.status = '400 Bad Request'
		else:
			permission = resource_descriptor.get_permission
			if permission == eapptools.ACCESS_NONE or (permission == eapptools.ACCESS_ADMIN and not users.is_current_user_admin()):
				self.response.status = '403 Not Authorized'
			else:
				entity_class = resource_descriptor.entity_class
			
				if not key:
					result = entity_class.find_all()
					logger.debug('Result: %s', result)
				else:
					result = entity_class.find(key)
				if not result:
					self.response.status = '404 Not Found'
				else:
					r = eapptools.model.to_json(result)
					logger.debug("Result: %s", r)
					self.response.content_type = "application/json"
					self.response.write(r)
	
	def post(self):
		logger.info("received post request: %s ", self.request.body)
		(resource_descriptor, key) = self._get_resource_descriptor(self.request.path)
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
				logger.debug("Data: %s", data)
				try:
					if key:
						entity = entity_class.find(key)
						if entity:
							entity.copy_from_dict(data)
							logger.debug("Updating %s", entity)
						else:
							entity = entity_class.create(data)
							logger.debug("Inserting %s", entity)
						entity.validate()
						entity.put()
				except val.ValidationError as e:
					self.response.status = '400 Bad Request'
					self.response.content_type = "application/json"
					response_message = ErrorResponse(val.ERR_VALIDATION, e.result).to_json()
					logger.debug("Error message: %s", response_message)
					self.response.write(response_message)
			
	def delete(self):
		logger.info("received delete request: %s ", self.request.body)
		(resource_descriptor, key) = self._get_resource_descriptor(self.request.path)
		if not resource_descriptor or not key:
			self.response.status = '400 Bad Request'
		else:
			permission = resource_descriptor.delete_permission
			if permission == eapptools.ACCESS_NONE or (permission == eapptools.ACCESS_ADMIN and not users.is_current_user_admin()):
				self.response.status = '403 Not Authorized'
			else:
				entity_class = resource_descriptor.entity_class
				try:
					entity = entity_class.find(key)
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