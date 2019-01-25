import unittest
import os
import json, pdb

from .contexts import create_api_server, QuestionerStorage

class TestMeetupsEndpoint(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()

        self.storage = QuestionerStorage()
                
    def test_endpoint_create_meetup_returns_json(self):
        """Test API returns error if content_type is incorrect in request"""
        res = self.client.post(
            'api/v1/meetups',
            data = json.dumps({
                "topic": "Q1 Meetup",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/jsony'
        )
        self.assertTrue(res.is_json)
    
    def test_endpoint_create_meetup_returns_error_if_content_type_wrong(self):
        """Test API returns error if content_type is incorrect in request"""
        res = self.client.post(
            'api/v1/meetups',
            data = json.dumps({
                "topic": "Q1 Meetup",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/jsony'
        )
        expected_output = {
            'status': 400,
            'error': 'Invalid Content_Type request header'
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_create_meetup_returns_error_if_no_request_data(self):
        """Test API returns error if no data is present in request"""
        res = self.client.post(
            'api/v1/meetups',
            data = json.dumps({}),
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "No data provided"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_create_meetup_returns_error_if_no_json_request_data_and_content_type_is_json(self):
        """Test API returns error if content_type is json and no json data in request"""
        res = self.client.post(
            'api/v1/meetups',
            data = {},
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "Request data invalid! No JSON data!"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_create_meetup_that_method_save_returns_error_if_db_save_not_successful(self):
        """Test API returns error if there was a problem saving new meetup to db """
        res = self.client.post(
            'api/v1/meetups',
            data = json.dumps({
                "topic": "Q1 Meetup",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        expected_output = {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

        if 'error' in res.json:
            self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
            self.assertEqual(res.status_code, 503, '503 status code not returned')
    
    def test_meetup_creation(self):
        """Test API can create a meetup (POST request)"""
        res = self.client.post('api/v1/meetups',
                                data = json.dumps({
                                    "topic": "Q1 Meetup",
                                    "location": "Nairobi",
                                    "happeningOn": "17/01/2019",
                                    "tags": []
                                }),
                                content_type='application/json'
        )

        self.assertEqual(res.status_code, 201)

    def test_endpoint_create_question(self):
        """Test API can create a question (POST request)"""
        res = self.client.post('api/v1/questions',
                                data = json.dumps({ 
                                    "createdBy": "001",
                                    "meetup": "Q1 Meetup",
                                    "title": 'Test title',
                                    "body": "Swali langu ni je",
                                    "votes": 0
                                }),
                                content_type='application/json'
        )       

        self.assertEqual(res.status_code, 201)

    # def test_endpoint_make_rsvp_is_reachable(self):
    #     """Test API can create a rsvp for user (POST request)"""
    #     res = self.client.post('api/v1/meetups/1/rsvps', data = {   "meetup": "Q1 Meetup",
    #                                                                 "user": 'Test user',
    #                                                                 "response": "Yes | No | Maybe",
    #                                                             })       

    #     self.assertEqual(res.status_code, 202)
    
    def test_endpoint_make_rsvp_returns_json(self):
        """Test API endpoint returns a json response"""
        res = self.client.post(
            'api/v1/meetups/1/rsvps',
            data = json.dumps({
                "meetup": "Q1 Meetup",
                "user": 'Test user',
                "response": "Yes | No | Maybe",
            })
        )       

        self.assertTrue(res.is_json)
    
    def test_endpoint_make_rsvp_returns_error_if_meetup_id_not_exist(self):
        """Test API endpoint returns a json response"""
        meetup_id = 100
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup_id),
            data = json.dumps({
                "meetup": "Q1 Meetup",
                "user": 'Test user',
                "response": "Yes | No | Maybe",
            })
        )       
        
        expected_output = {
            "status": 404,
            "error": "Meetup with id {} not found".format(meetup_id)
        }

        self.assertTrue(
            all(item in res.json.items() for item in expected_output.items()),
            'Output received does not match output expected'     
        )
        self.assertEqual(res.status_code, 404)

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

        self.assertEqual(res.status_code, 200)
    
    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
