# import pdb

import unittest
import os
import json

from .contexts import validate_request_data, validate_route_param

class TestUtilitiesFunctions(unittest.TestCase):
    """This class represents the utilities test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.validate_request_data = validate_request_data
        self.validate_route_param = validate_route_param

    def test_validate_required_fields_present(self):
        """Test that required fields are present"""
        input_meetup =  [   {   "topic": "Required is present",
                                "happeningOn": "17/01/2019",
                                "location" : "Nairobi",
                                # "created_by" : ""
                            },
                            {
                                "images": [],
                                "tags" : []
                            }
                        ]
        input_2 = ['topic', 'location', 'happeningOn']

        output = self.validate_request_data(input_meetup, input_2)

        if 'error' not in output:
            self.assertIn("topic", output)
            self.assertIn("happeningOn", output)
            self.assertIn("location", output)

    def test_validate_required_fields_not_empty(self):
        """Test that required fields are not empty"""
        input_meetup =  [   {   "topic": "Required Not Empty",
                                "happeningOn": "17/01/2019",
                                "location" : "",
                                # "created_by" : ""
                            },
                            {
                                "images": [],
                                "tags" : []
                            }
                        ]
        input_2 = ['topic', 'location', 'happeningOn']

        output = self.validate_request_data(input_meetup, input_2)

        self.assertIn('error', output)
        self.assertIn('Required field(s) empty', output['error'], 'A required field is empty')
        
    def test_validate_remove_empty_non_required(self):
        """Test that empty non required fields are removed from request data"""
        
        input_meetup =  [   {   "topic": "Removed empty Others",
                                "happeningOn": "17/01/2019",
                                "location" : "Nairobi"
                            },
                            {
                                "images": [],
                                "tags" : ""
                            }
                        ]
        input_2 = ['topic', 'location', 'happeningOn']
        expected_output = { "topic": "Removed empty Others",
                            "happeningOn": "17/01/2019",
                            "location": "Nairobi",
                            "images": []
                        }

        output = self.validate_request_data(input_meetup, input_2)

        self.assertTrue(all(item in output.items() for item in expected_output.items()))       

    def test_method_validate_route_param_returns_int(self):
        """Test that the route param can be converted to int"""
        input_1 = '1'

        output = self.validate_route_param(input_1)

        assert type(output) == int
    
    def test_method_validate_route_param_returns_error_if_not_int(self):
        """Test that the route param can be converted to int"""
        input_1 = ''

        output = self.validate_route_param(input_1)

        self.assertIn('error', output)

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
