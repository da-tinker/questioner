import unittest
import os
import json

from .contexts import create_api_server, rsvp_validate_request_data, is_meetup_id_invalid

class TestRsvpsEndpointFunctions(unittest.TestCase):
    """This class represents the rsvp views test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = create_api_server("testing")
        self.rsvp_validate_request_data = rsvp_validate_request_data
        self.rsvp_is_meetup_id_invalid = is_meetup_id_invalid
        
    def test_validate_rsvp_required_fields_present(self):
        """Test that required fields are present"""
        req_data = {    "meetup": 1,
                        "user": 1,
                        # "response": "maybe"
                    }

        output = self.rsvp_validate_request_data(req_data)

        if not output['error']:
            self.assertIn("response", output)

    def test_validate_rsvp_required_fields_not_empty(self):
        """Test that required fields are not empty"""
        req_data = {    "meetup": 1,
                        "user": '',
                        "response": "maybe"
                    }

        output = self.rsvp_validate_request_data(req_data)
        
        self.assertIn('error', output)
        self.assertIn('Required field(s) empty', output['error'], 'A required field is empty')
        
    def test_is_meetup_id_invalid_returns_true_if_meetup_exists(self):
        """Test that meetup with specified id exists"""

        self.assertTrue(self.rsvp_is_meetup_id_invalid(1))

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
