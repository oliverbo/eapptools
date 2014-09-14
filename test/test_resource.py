import unittest
import eapptools
from eapptools import resource
from eapptools import user_manager

class ResourceTestCase(unittest.TestCase):
	def setUp(self):
		config = eapptools.get_config()
		
				
	def tearDown(self):
		pass
		
	def testPathElements(self):
		mapping = {
			'/api/user' : resource.ResourceDescriptor(user_manager.User, eapptools.ACCESS_USER, eapptools.ACCESS_USER, eapptools.ACCESS_USER,
			('parent_id', 'id'))
		}
					
		(resource_descriptor, param) = resource._get_resource_descriptor("/api/user/13241311/5162526", mapping)
		self.assertEqual('5162526', param['id'])
		self.assertEqual('13241311', param['parent_id'])
				
if __name__ == '__main__':
    unittest.main()
