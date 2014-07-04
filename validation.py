# Utilities to handle validation

ERR_INVALID_NUMBER = 1000
ERR_DATA_MISSING = 1001
ERR_DUPLICATE_KEY = 1002

VALIDATION_ERRORS = {
	ERR_INVALID_NUMBER : "Invalid Number",
	ERR_DATA_MISSING : "Mandatory field missing",
	ERR_DUPLICATE_KEY : "Duplicate Key"
}

class ValidationError(Exception):
	result = None

	def __init__(self, result):
		self.result = result

class ValidationResult:
	errorCode = 0;
	errorMessage = None;
	field = None;
	
	def __init__(self, error_code, field = None, error_message = None):
		self.errorCode = error_code;
		self.field = field
		if error_message:		
			self.errorMessage = error_message
		elif error_code in VALIDATION_ERRORS:
			self.errorMessage = VALIDATION_ERRORS[error_code]
				
def _append_to_result(result, item):
	if result:
		result.append(item)
						
def get_string(data_dict, name, result, mandatory = False):
	"""Returns a string safely from the dictionary"""
	string_value = None
	if name in data_dict:
		string_value = data_dict[name]
	else:
		string_value = None
		
	if (mandatory and not string_value):
		_append_to_result(result, ValidationResult(ERR_DATA_MISSING, "uniqueName"))
		
	return string_value
			
def get_int(data_dict, name, result, mandatory = False):
	"""Validates and converts an integer value"""
	int_value = None
	if name in data_dict:
		value = data_dict[name]
		if value:
			try:
				venue.priceLevel = int(data_dict['priceLevel'])
			except:
				_append_to_result(result, ValidationResult(ERR_INVALID_NUMBER, name))
	return int_value
