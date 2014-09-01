# basic environment setting for web tools

import os
import logging

logger = logging.getLogger("eapptools")

RUNMODE_DEV = 'DEV'
RUNMODE_PROD = 'PROD'

if not 'SERVER_SOFTWARE' in os.environ or os.environ['SERVER_SOFTWARE'].startswith('Dev'):
	RUNMODE = RUNMODE_DEV
else:
	RUNMODE = RUNMODE_PROD
	
logger.info("RUNMODE=%s", RUNMODE)

# config paramater names
CFG_GLOBAL_APP_DIR = 'global_app_dir'
CFG_HTML_DIR = 'html_dir'
CFG_DEFAULT_PAGE = 'default_page'
CFG_RESOURCE_MAPPING = 'resource_mapping'
CFG_PAGE_MAPPING = 'page_mapping'
CFG_DEV_JS = "dev_js"
CFG_PROD_JS = "prod_js"

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


