import unittest
import os
import json

from .contexts import QuestionerStorage

class TestQuestionerStorageFunctions(unittest.TestCase):
    """This class represents the storage test case for Questioner"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_api_server("testing")
        self.storage = QuestionerStorage()
        
    def test_storage_is_instance_of_QuestionerStorage(self):
        """Test that storage object is instantiated"""
        self.assertIsInstance(self.storage, QuestionerStorage, 'Storage Not Instantiated')

    def test_storage_has_property_meetups_list(self):
        """Test that storage object has meetups list property"""
        self.assertTrue(self.storage.message_list == [])

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
