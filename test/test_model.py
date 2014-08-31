# Test for the model class

import unittest
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from eapptools import model
from eapptools import validation as val

class TestModel(model.ModelBase):
	"""A test model class"""
	name = ndb.StringProperty()
	
	@classmethod
	def parent_key(cls):
		"""Returns the parent key - by default the base key"""
		return ndb.Key("Base", "user")
	
	def copy_from_dict(self, data_dict):
		result = []
		self.uniqueName = val.get_string(data_dict, "uniqueName", result)
		self.name = val.get_string(data_dict, "name", result)
	
	
class ModelTestCase(unittest.TestCase):
	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		
	def tearDown(self):
		self.testbed.deactivate()	
		
	def testCreateEntity(self):
		test_model = TestModel.create({"uniqueName" : "1", "name" : "Test"})
		self.assertEqual("1", test_model.uniqueName)
		self.assertEqual("Test", test_model.name)
		
if __name__ == '__main__':
    unittest.main()
		
