# Handles loaging of a page

import logging
import json

import eapptools
import webapp2
from google.appengine.api import users
import jinja2

logger = logging.getLogger("page_handler")

_JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader('/'),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = False
)

class PageDescriptor:
	"""Describes a page of the site"""
	file = None
	access = eapptools.ACCESS_ALL
	
	def __init__(self, file = None, access = eapptools.ACCESS_ALL):
		"""Initializes a file descriptor with file mapping an access """
		self.file = file
		self.access = access

class PageHandler(webapp2.RequestHandler):
	"""handles loading of a page"""
	def get(self):
		logger.info("Requested page: '%s'", self.request.path)
		
		if self.request.path == '/':
			page = self.app.config.get(eapptools.CFG_DEFAULT_PAGE)
		else:
			page = self.request.path
			
		mapping = self.app.config.get(eapptools.CFG_PAGE_MAPPING)
		
		if page in mapping:
			page_descriptor = mapping[page]
			
			user = users.get_current_user()		
			
			# Checking authorization
			if page_descriptor.access == eapptools.ACCESS_NONE:
				logger.info("No access to page")
				self.response.status = '403 Not authorized'
			elif page_descriptor.access == eapptools.ACCESS_USER and not user:
				logger.info("Page only available to authorized users")
				self.response.status = '403 Not authorized'
			elif page_descriptor.access == eapptools.ACCESS_ADMIN and not users.is_current_user_admin():
				logger.info("Page only available to authorized admins")
				self.response.status = '403 Not authorized'
				
			file = page_descriptor.file
			if not file:
				# by default set file to same path as requested page
				file = page
				
			global_html_dir = self.app.config.get(eapptools.CFG_GLOBAL_APP_DIR) + '/' + self.app.config.get(eapptools.CFG_HTML_DIR)
				
			template = _JINJA_ENVIRONMENT.get_template(global_html_dir + '/' + file)
			
			# compose page info
			page_info = {
				'logoutURI' : users.create_logout_url('/'),
				'loginURI' : users.create_login_url('/')
			}
			if user:
				page_info["userName"] = user.nickname()
        	
			if users.is_current_user_admin():
				page_info["isAdmin"] = True;
				
			template_values = {'pageInfo' : _create_page_module(page_info)}
			self.response.write(template.render(template_values))
		else:
			self.response.status = '404 not found'
        
def _create_page_module(values):
	"""Creates JavaScript Code for a Angular module that includes the passed parameters as a JSON object"""
	
	code = "angular.module('pageModule', []).value('pageInfo',"
	value_json = json.dumps(values)
	code = code + value_json + ');'
	
	logger.info(code)
	
	return code
	