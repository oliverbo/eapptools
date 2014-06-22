import os
import urllib
import logging
import json

from google.appengine.api import users
import jinja2
import apptools

AUTH_NONE = 0
AUTH_USER = 1
AUTH_ADMIN = 2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader('/'),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = False
)

logger = logging.getLogger("page_handler")
    
def static_page(request_handler, page_name, page_dir = 'html', auth_mode = AUTH_NONE):
    user = users.get_current_user()
    
    logger.info("auth_mode: %d", auth_mode)
    logger.debug("Root Dir %s", apptools.web_root)
    if user:
    	logger.info('authenticated user: %s', user.nickname())
    	logger.info('user is admin: %s', users.is_current_user_admin())
    else:
    	logger.info('no authenticated user')
                
    if user or auth_mode == AUTH_NONE:
        if not users.is_current_user_admin() and auth_mode == AUTH_ADMIN:
			request_handler.response.status = '401 Not Authorized'
			return
        template = JINJA_ENVIRONMENT.get_template(apptools.web_root + '/' + page_name)
        
        # compose page info
        page_info = {
        	'logoutURI' : users.create_logout_url('/'),
        	'loginURI' : users.create_login_url('/')
        }
        if user:
        	page_info["userName"] = user.nickname()
        	
        if users.is_current_user_admin():
        	page_info["isAdmin"] = True;
        	
        # return template
        	
        template_values = {'pageInfo' : _create_page_module(page_info)}
        	
        request_handler.response.write(template.render(template_values))
    else:
        logger.info('No user authenticated')
        request_handler.redirect(users.create_login_url(request_handler.request.path))
        
def _create_page_module(values):
	"""Creates JavaScript Code for a Angular module that includes the passed parameters as a JSON object"""
	
	code = "angular.module('pageModule', []).value('pageInfo',"
	value_json = json.dumps(values)
	code = code + value_json + ');'
	
	logger.info(code)
	
	return code
	
	