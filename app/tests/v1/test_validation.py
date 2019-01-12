import unittest
import os
import json

from .contexts import create_api_server, validate_request_data

class TestMeetupsEndpointFunctions(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.meetup_validate_request_data = validate_request_data
        
                
    def test_validate_meetup_fields(self):
        """Test that required fields are present"""
        req_data =  {    "topic": "Q1 Meetup",
                        "happeningOn": "17/01/2019",
                        "location" : "Nairobi",
                        "images": [],
                        "Tags": [],
                        "created_by" : ""
                    }

        output = self.meetup_validate_request_data(req_data)

        self.assertIn("location", output)


    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
