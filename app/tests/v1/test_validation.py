import unittest
import os
import json

from .contexts import create_api_server, validate_request_data

class TestMeetupsEndpointFunctions(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_api_server("testing")
        self.meetup_validate_request_data = validate_request_data
        
    def test_validate_meetup_required_fields_present(self):
        """Test that required fields are present"""
        req_data =  {   "topic": "Q1 Meetup",
                        "happeningOn": "17/01/2019",
                        "location" : "Nairobi",
                        "images": [],
                        "Tags": [],
                        "created_by" : ""
                    }

        output = self.meetup_validate_request_data(req_data)

        self.assertIn("location", output)

    def test_validate_meetup_required_fields_not_empty(self):
        """Test that required fields are not empty"""
        req_data =  {    "topic": "Q1 Meetup",
                        "happeningOn": "17/01/2019",
                        "location": "Nairobi",
                        "images": [],
                        "Tags": [],
                        "created_by" : ""
                    }

        output = self.meetup_validate_request_data(req_data)
        
        self.assertIn('error', output)
        self.assertIn('Required field(s) empty', output['error'], 'A required field is empty')
        


    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
