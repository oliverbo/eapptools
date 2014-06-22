# Base class for handlers for NDB data access

class DataHandler:
	
	# queries all data
	def query(self):
		pass
		
	def find(self, key):
		"""Finds a record uniquely identified by key or None if the key doesn't exist"""
		pass
		
	# saves an object
	def save(self, data, key = None):
		"""Saves a record. If no key is specified or the key does not yet exists, a new record is created"""
		pass
		
	def delete(self, key):
		"""Deletes a record identified by the key"""
		pass
		
	def delete_all(self):
		"""Deletes all records in the data store"""
		pass
		
	def export_data(self):
		"""Exports the all records"""
		pass
		
	def import_data(self, data):
		"""Imports the records in the JSON data structure"""
		pass
