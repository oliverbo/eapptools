# Test for the model class

import unittest
import datetime
import json
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from eapptools import model
from eapptools import validation as val

class TestModel(model.ModelBase):
	"""A test model class"""
	name = ndb.StringProperty()
	int = ndb.IntegerProperty()
	date = ndb.DateProperty()
	datetime = ndb.DateTimeProperty()
	time = ndb.TimeProperty()
	
	@classmethod
	def parent_key(cls):
		"""Returns the parent key - by default the base key"""
		return ndb.Key("Base", "user")
	
	def copy_from_dict(self, data_dict):
		result = []
		self.id = val.get_string(data_dict, "id", result)
		self.name = val.get_string(data_dict, "name", result)
	
	
class ModelTestCase(unittest.TestCase):
	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		
	def tearDown(self):
		self.testbed.deactivate()	
		
	def testCreateEntity(self):
		test_model = TestModel.create({"id" : "1", "name" : "Test"})
		self.assertEqual("1", test_model.id)
		self.assertEqual("Test", test_model.name)
		test_key = test_model.put()
		
	def testJsonConverter(self):
		test_model = TestModel.create({"id" : "1"})
		test_model.name = "Test"
		test_model.int = 5
		test_model.date = datetime.date(1964, 10, 8)
		test_model.datetime = datetime.datetime(2014, 9, 1, 14, 55, 27)
		test_model.time = datetime.time(12, 22, 56)
		test_key = test_model.put()
		test_model_2 = test_key.get()
		json_data = test_model.to_json()
		data_dict = json.loads(json_data)
		self.assertEqual(5, data_dict["int"])
		self.assertEqual('1964-10-08', data_dict["date"])
		self.assertEqual('2014-09-01T14:55:27', data_dict["datetime"])
		self.assertEqual('12:22:56', data_dict["time"])
		
if __name__ == '__main__':
    unittest.main()
		
