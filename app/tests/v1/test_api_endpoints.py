import unittest
import os
import json
from .contexts import create_api_server


class MeetupsEndpointTestCase(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server(config_name="testing")
        self.client = self.app.test_client
        self.meetup = { "id": 1,
                        "createdOn": "10/01/2019",
                        "location": "Nairobi",
                        "images": [],
                        "topic": "Q1 Meetup",
                        "happeningOn": "17/01/2019",
                        "Tags": [],
                    }
        
    def test_meetup_creation(self):
        """Test API can create a meetup (POST request)"""
        res = self.client().post('/meetups/', data=self.meetup)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Q1 Meetup', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
