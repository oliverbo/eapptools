# JavaScript utility functions

import eapptools

def create_java_script_references(config):
	"""Creates the references for JavaScript"""
	
	if eapptools.RUNMODE == eapptools.RUNMODE_DEV:
		js_list = config[eapptools.CFG_DEV_JS]
	else:
		js_list = config[eapptools.CFG_PROD_JS]
		
	code = ''
	if js_list:
		for js_script in js_list:
			code = code + '<script src="%s"></script>'%js_script
				
	return code