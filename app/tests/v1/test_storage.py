import pdb

import unittest
import os
import json
import datetime

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

    def test_storage_has_property_meetup_list(self):
        """Test that storage object has meetups list property"""
        self.assertTrue(self.storage.meetup_list == [])
    
    def test_storage_has_property_rsvp_list(self):
        """Test that storage object has rsvps list property"""
        self.assertTrue(self.storage.rsvp_list == [])
    
    def test_storage_has_property_question_list(self):
        """Test that storage object has rsvps list property"""
        self.assertTrue(self.storage.question_list == [])
            
    def test_storage_has_method_property_save_item(self):
        """Test that storage object has property save_item method"""
        self.assertTrue('save_item' in dir(self.storage))

    def test_storage_has_method_property_generate_id(self):
        """Test that storage object has property generate_id method"""
        self.assertTrue('generate_id' in dir(self.storage))
    
    def test_storage_has_method_property_check_id_unique(self):
        """Test that storage object has property check_id_unique method"""
        self.assertTrue('check_id_unique' in dir(self.storage))
    
    def test_storage_has_method_property_get_all_records(self):
        """Test that storage object has property get_all_recordsmethod"""
        self.assertTrue('get_all_records' in dir(self.storage))

    def test_storage_has_method_property_increment_generated_non_unique_id(self):
        """Test that storage object has property increment_generated_non_unique_id method"""
        self.assertTrue('increment_generated_non_unique_id' in dir(self.storage))
    
    def test_storage_method_generate_id_returns_new_id(self):
        """Test that generate_id() returns id plus 1 of list length"""
        input_list = []
        input_list_2 = ['item_1', 'item_2']
        
        output = self.storage.generate_id(input_list)
        output_2 = self.storage.generate_id(input_list_2)

        self.assertEqual(1, output)
        self.assertEqual(3, output_2)
    
    def test_storage_method_check_unique_id_returns_true(self):
        """Test that generated is unique"""
        input_1 = 3
        input_2 = [{
                        "id": 1,
                        "topic": "Q1 Meetup",
                        "location": "Nairobi",
                        "happeningOn": "17/01/2019",
                        "images": [],
                        "Tags": [],
                        "createdOn": "10/01/2019"
                    }, {    "id": 3,
                            "topic": "Review Meetup",
                            "location": "Westend Sterner",
                            "happeningOn": "17/01/2019",
                            "images": [],
                            "Tags": [],
                            "createdOn": "10/01/2019"                    
                    }]

        
        output = self.storage.check_id_unique(input_1, input_2)

        self.assertEqual(False, output)
    
    def test_storage_method_increment_generated_id_increments_id_by_one(self):
        """Test that generated id is again incremented by one if found to be not unique"""
                
        output = self.storage.increment_generated_non_unique_id(3)

        self.assertEqual(4, output)

    def test_storage_method_set_id_and_creation_time_adds_attributes_to_item(self):
        """Test that storage method set_id_and_creation_time adds attributes to list item"""
        input_1 = 4
        input_2 = 1547334591.917148
        input_3 =   {  
                        "topic": "VIPIPI Meetup",
                        "location": "Westend Sterner",
                        "happeningOn": "17/01/2019",
                        "images": [],
                        "Tags": [],
                        "created_by": "Tester"
                    }

        output = self.storage.set_id_and_creation_time(input_1, input_2, input_3) 
        self.assertIn('id', output)
        self.assertEqual(4, output['id'])
        self.assertIn('createdOn', output)
        self.assertEqual(datetime.datetime.fromtimestamp(input_2).strftime('%d-%m-%Y'), output['createdOn'])

    def test_storage_method_add_to_list_appends_new_item_record_to_list(self):
        """Test that the new meetup record is added to the items list"""
        input_1 = {
                    "topic": "VIPIPI Meetup",
                    "location": "Westend Sterner",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": [],
                    "created_by": "Tester"
                }
        
        input_2 = [{"id": 1,
                    "topic": "Q1 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": [],
                    "createdOn": "10/01/2019"
        }]

        expected_output = [{    "id": 1,
                                "topic": "Q1 Meetup",
                                "location": "Nairobi",
                                "happeningOn": "17/01/2019",
                                "images": [],
                                "Tags": [],
                                "createdOn": "10/01/2019"
                            }, {    "topic": "VIPIPI Meetup",
                                    "location": "Westend Sterner",
                                    "happeningOn": "17/01/2019",
                                    "images": [],
                                    "Tags": [],
                                    "created_by": "Tester"            
        }]
        
        output = self.storage.add_to_list(input_1, input_2)
        self.assertEqual(expected_output, output)
        
    def test_storage_method_add_new_item_record_returns_new_item(self):
        """Test that newly created record is returned by add_new_item_record on successful save"""

        input_1 = {   
            "topic": "Q1 Meetup",
            "location": "Nairobi",
            "happeningOn": "17/01/2019",
            "images": [],
            "Tags": []
        }

        input_2 = []

        expected_output = { "id": 1,
                            "topic": "Q1 Meetup",
                            "location": "Nairobi",
                            "happeningOn": "17/01/2019",
                            "images": [],
                            "Tags": [],
                        }

        output = self.storage.add_new_item_record('meetups', input_1, input_2)

        self.assertTrue(all(item in output.items() for item in expected_output.items()))
    
    def test_storage_method_save_item_returns_new_item(self):
        """Test that newly created record is returned by save_item on successful save"""

        input_1 = {   #"id": 1,
                    "topic": "Q1 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": [],
                }

        expected_output = { #"id": 1,
                            "topic": "Q1 Meetup",
                            "location": "Nairobi",
                            "happeningOn": "17/01/2019",
                            "images": [],
                            "Tags": [],
                        }

        output = self.storage.save_item('meetups', input_1, 'add_new')
        self.assertTrue(all(item in output.items() for item in expected_output.items()))

    def test_storage_method_get_all_records_returns_list_of_records(self):
        """Test that a list of item records is returned"""

        output = self.storage.get_all_records('meetups')
        # pdb.set_trace()
        # self.assertIs(output, list()) # Gives error: AssertionError: [] is not [] // bug??
        assert type(output) == list
    
    def test_storage_method_get_record_returns_record_of_type_dict(self):
        """Test that a record(dict) is returned"""
        input_1 = { "topic": "Q2 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": []
                }
        
        input_2 = {
                    "topic": "Q1 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": []
                }

        output_1 = self.storage.save_item('meetups', input_1, 'add_new')
        output_2 = self.storage.save_item('meetups', input_2, 'add_new')

        output = self.storage.get_record(output_1['id'], self.storage.meetup_list)
        output_ = self.storage.get_record(output_2['id'], self.storage.meetup_list)
        
        assert type(output) == dict
        assert type(output_) == dict
    
    def test_storage_method_get_record_returns_record_of_specified_id(self):
        """Test that a record(dict) of specified id is returned"""

        input_1 = { "topic": "Q2 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": []
                }
        
        input_2 = {
                    "topic": "Q1 Meetup",
                    "location": "Nairobi",
                    "happeningOn": "17/01/2019",
                    "images": [],
                    "Tags": []
                }

        output_1 = self.storage.save_item('meetups', input_1, 'add_new')
        output_2 = self.storage.save_item('meetups', input_2, 'add_new')

        output = self.storage.get_record(output_1['id'], self.storage.meetup_list)
        output_ = self.storage.get_record(output_2['id'], self.storage.meetup_list)
        
        self.assertEqual(output_1['id'], output['id'])
        self.assertEqual(output_2['id'], output_['id'])

    def test_storage_method_get_record_returns_error_if_record_not_found(self):
        """Test that a record(dict) is returned"""

        output = self.storage.get_record(102, self.storage.meetup_list)

        self.assertIn('error', output)

    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
