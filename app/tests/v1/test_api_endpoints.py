import unittest
import os
import json #, pdb

from .contexts import create_api_server, QuestionerStorage

class TestMeetupsEndpoint(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()

        self.storage = QuestionerStorage()
                
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

    # def test_endpoint_make_rsvp_is_reachable(self):
    #     """Test API can create a rsvp for user (POST request)"""
    #     res = self.client.post('api/v1/meetups/1/rsvps', data = {   "meetup": "Q1 Meetup",
    #                                                                 "user": 'Test user',
    #                                                                 "response": "Yes | No | Maybe",
    #                                                             })       

    #     self.assertEqual(res.status_code, 202)

    # def test_endpoint_upvote_question_is_reachable(self):
    #     """Test API can upvote a question (PATCH request)"""
    #     input_1 = {
    #         "meetup": "Q1 Meetup",
    #         "title": 'Test title',
    #         "body": "Swali langu ni je",
    #         "votes": "0"
    #     }
    #     output = self.storage.save_item('questions', input_1, 'add_new')
    #     # pdb.set_trace()
    #     res = self.client.patch('api/v1/questions/{}/upvote'.format(output['id']))       

    #     self.assertEqual(res.status_code, 202)

    # def test_endpoint_downvote_question_is_reachable(self):
    #     """Test API can downvote a question (PATCH request)"""
    #     res = self.client.patch('api/v1/questions/1/downvote', data = {    "meetup": "Q1 Meetup",
    #                                                                     "title": 'Test title',
    #                                                                     "body": "Swali langu ni je",
    #                                                                     "votes": "0"
    #                                                             })       

    #     self.assertEqual(res.status_code, 202)

    # def test_endpoint_fetch_a_meetup_is_reachable(self):
    #     """Test API can get a specific meetup record (GET request)"""
    #     res = self.client.get('api/v1/meetups/1')       

    #     self.assertEqual(res.status_code, 203)

    def test_endpoint_get_all_meetups_is_reachable(self):
        """Test API can fetch all upcoming meetup records (GET request)"""
        res = self.client.get('api/v1/meetups/upcoming/')       

        self.assertEqual(res.status_code, 203)
    
    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
