import unittest
import os
import json

from .contexts import create_api_server

class TestMeetupsEndpoint(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
                
    def test_meetup_creation(self):
        """Test API can create a meetup (POST request)"""
        res = self.client.post('api/v1/meetups', data = { "id": 1,
                                                            "createdOn": "10/01/2019",
                                                            "location": "Nairobi",
                                                            "images": [],
                                                            "topic": "Q1 Meetup",
                                                            "happeningOn": "17/01/2019",
                                                            "Tags": [],
                                                        })
        self.assertEqual(res.status_code, 202)

    def test_endpoint_create_question(self):
        """Test API can create a question (POST request)"""
        res = self.client.post('api/v1/questions', data = { "createdOn": "storage to provide",
                                                            "createdBy": "001",
                                                            "meetup": "Q1 Meetup",
                                                            "title": 'Test title',
                                                            "body": "Swali langu ni je",
                                                            "votes": "17/01/2019"
                                                        })       

        self.assertEqual(res.status_code, 202)
    
    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
