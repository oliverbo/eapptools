# basic environment setting for web tools

import logging

logger = logging.getLogger("eapptools")

# config paramater names
CFG_GLOBAL_APP_DIR = 'global_app_dir'
CFG_HTML_DIR = 'html_dir'
CFG_DEFAULT_PAGE = 'default_page'
CFG_RESOURCE_MAPPING = 'resource_mapping'
CFG_PAGE_MAPPING = 'page_mapping'

_config = {
	CFG_GLOBAL_APP_DIR : '/',
	CFG_HTML_DIR : 'html',
	CFG_DEFAULT_PAGE : '/index.html'
}

# Access levels
ACCESS_NONE = 0
ACCESS_ALL = 1
ACCESS_ADMIN = 2
ACCESS_USER = 3


def get_config():
	return _config


