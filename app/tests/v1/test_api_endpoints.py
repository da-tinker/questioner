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
        """Test API returns json data"""
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

    def test_endpoint_create_question_returns_json(self):
        """Test API returns json data"""
        res = self.client.post('api/v1/questions')       
        self.assertTrue(res.is_json)

    def test_endpoint_create_question_returns_error_if_no_request_data(self):
        """Test API returns error if no data is present in request"""
        res = self.client.post(
            'api/v1/questions',
            data = json.dumps({}),
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "No data provided"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_create_question_returns_error_if_no_json_request_data_and_content_type_is_json(self):
        """Test API returns error if content_type is json and no json data in request"""
        res = self.client.post(
            'api/v1/questions',
            data = {},
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "Request data invalid! No JSON data!"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items() ))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_create_question_that_method_save_returns_error_if_db_save_not_successful(self):
        """Test API returns error if there was a problem saving new question to db """
        res = self.client.post(
            'api/v1/questions',
            data = json.dumps({
                "createdBy": 1,
                "meetup": 1,
                "title": 'Test title',
                "body": "Swali langu ni je",
                "votes": 0
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
    
    def test_endpoint_create_question_creates_new_question_and_returns_created_question(self):
        """Test API can create a question and returns the created question (POST request)"""
        res = self.client.post('api/v1/questions',
                                data = json.dumps({ 
                                    "createdBy": 1,
                                    "meetup": 1,
                                    "title": 'Test title',
                                    "body": "Swali langu ni je",
                                    "votes": 0
                                }),
                                content_type='application/json'
        )       
        expected_output = {
            "status": 201,
            "data": [
                {
                    "user": 1,  # user who posted the question
                    "meetup": 1,  # meetup record primary key
                    "title": 'Test title',
                    "body": "Swali langu ni je"
                }
            ]
        }
        
        self.assertEqual(res.json['status'], expected_output['status'])
        self.assertTrue(all(item in res.json['data'][0].items() for item in expected_output['data'][0].items()))
        self.assertEqual(res.status_code, 201)

    def test_endpoint_upvote_question_returns_json(self):
        """Test API gives a json response (PATCH request)"""
        # First, create a question record
        input_1 = {
            "meetup": "Q1 Meetup",
            "title": 'Test title',
            "body": "Swali langu ni je",
            "votes": "0"
        }
        output = self.storage.save_item('questions', input_1, 'add_new')

        # Next, test the upvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/upvote'.format(output['id'])
        )

        self.assertTrue(res.is_json)
    
    def test_endpoint_upvote_question_increments_votes_for_question_by_one(self):
        """Test API increments question's votes by one (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 200,
            "data": [
                {
                    "meetup": "Q1 Meetup",
                    "title": 'Test title',
                    "body": "Swali langu ni je",
                    "votes": 3
                }
            ]
        }
        # Then, create a question record
        input_1 = {
            "meetup": "Q1 Meetup",
            "title": 'Test title',
            "body": "Swali langu ni je",
            "votes": 2
        }        
        new_question_record = self.storage.save_item('questions', input_1, 'add_new')

        # Next, test the upvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/upvote'.format(new_question_record['id'])
        )

        self.assertEqual(res.json['status'], expected_output['status'])
        self.assertEqual(res.json['data'][0]['votes'], expected_output['data'][0]['votes'])
        self.assertEqual(res.status_code, 200)
    
    def test_endpoint_upvote_question_returns_error_if_route_param_invalid(self):
        """Test API returns an error if the route param is invalid (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 400,
            "error": 'Invalid route parameter'
        }
        
        # Next, test the upvote question endpoint
        res = self.client.patch(
            'api/v1/questions/invalid_param/upvote'
        )

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_upvote_question_returns_error_if_question_not_found(self):
        """Test API returns an error if the question id is not found (PATCH request)"""
        # Define the expected output
        inexistent_id = 19921
        
        expected_output = {
            "status": 404,
            "error": "No record found for id {}".format(inexistent_id)
        }
        
        # Next, test the upvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/upvote'.format(inexistent_id)
        )

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 404)
    
    def test_endpoint_downvote_question_returns_json(self):
        """Test API gives a json response (PATCH request)"""
        # First, create a question record
        input_1 = {
            "meetup": "Q1 Meetup",
            "title": 'Test title',
            "body": "Swali langu ni je",
            "votes": "0"
        }
        new_question_record = self.storage.save_item('questions', input_1, 'add_new')

        # Next, test the downvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/downvote'.format(new_question_record['id'])
        )

        self.assertTrue(res.is_json)
    
    def test_endpoint_downvote_question_decrements_votes_for_question_by_one(self):
        """Test API decrements question's votes by one (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 200,
            "data": [
                {
                    "meetup": "Q1 Meetup",
                    "title": 'Test title',
                    "body": "Swali langu ni je",
                    "votes": 1
                }
            ]
        }
        # Then, create a question record
        input_1 = {
            "meetup": "Q1 Meetup",
            "title": 'Test title',
            "body": "Swali langu ni je",
            "votes": 2
        }        
        new_question_record = self.storage.save_item('questions', input_1, 'add_new')

        # Next, test the downvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/downvote'.format(new_question_record['id'])
        )

        self.assertEqual(res.json['status'], expected_output['status'])
        self.assertEqual(res.json['data'][0]['votes'], expected_output['data'][0]['votes'])
        self.assertEqual(res.status_code, 200)
    
    def test_endpoint_downvote_question_does_not_decrement_if_votes_are_zero(self):
        """Test API does not decrement the votes if votes are zero (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 200,
            "data": [
                {
                    "meetup": "Q1 Meetup",
                    "title": 'Test title',
                    "body": "Swali langu ni je",
                    "votes": 0
                }
            ]
        }
        # Then, create a question record
        res_new_question = self.client.post('api/v1/questions',
                                                data=json.dumps({
                                                    "createdBy": 1,
                                                    "meetup": 1,
                                                    "title": 'Test title',
                                                    "body": "Swali langu ni je",
                                                    "votes": "0"
                                                }),
                                                content_type='application/json'
        )
        new_question_record = res_new_question.json['data'][0]

        # Next, test the downvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/downvote'.format(new_question_record['id'])
        )

        self.assertEqual(res.json['status'], expected_output['status'])
        self.assertEqual(res.json['data'][0]['votes'], expected_output['data'][0]['votes'])
        self.assertEqual(res.status_code, 200)
    
    def test_endpoint_downvote_question_returns_error_if_route_param_invalid(self):
        """Test API returns an error if the route param is invalid (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 400,
            "error": 'Invalid route parameter'
        }
        
        # Next, test the downvote question endpoint
        res = self.client.patch(
            'api/v1/questions/invalid_param/downvote'
        )

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)
    
    def test_endpoint_downvote_question_returns_error_if_question_not_found(self):
        """Test API returns an error if the question id is not found (PATCH request)"""
        # Define the expected output
        inexistent_id = 19921
        
        expected_output = {
            "status": 404,
            "error": "No record found for id {}".format(inexistent_id)
        }
        
        # Next, test the downvote question endpoint
        res = self.client.patch(
            'api/v1/questions/{}/downvote'.format(inexistent_id)
        )

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 404)

    def test_endpoint_make_rsvp_returns_json(self):
        """Test API endpoint returns a json response"""
        res = self.client.post('api/v1/meetups/1/rsvps')       

        self.assertTrue(res.is_json)
    
    def test_endpoint_make_rsvp_returns_error_if_no_request_data(self):
        """Test API returns error if no data is present in request"""
        # First, create a meetup record
        res_meetup = self.client.post(
            'api/v1/meetups',
            data=json.dumps({
                "topic": "RSVP the Meet",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]
        # pdb.set_trace()
        # Next, test the make rsvp endpoint
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup['id']),
            data=json.dumps({}),
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "No data provided"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)

    def test_endpoint_make_rsvp_returns_error_if_no_json_request_data_and_content_type_is_json(self):
        """Test API returns error if content_type is json and no json data in request"""
        # First, create a meetup record
        res_meetup = self.client.post(
            'api/v1/meetups',
            data=json.dumps({
                "topic": "RSVP the Meet",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]
        
        # Next, test the make rsvp endpoint
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup['id']),
            data={},
            content_type='application/json'
        )
        expected_output = {
            'status': 400,
            'error': "Request data invalid! No JSON data!"
        }

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)

    def test_endpoint_make_rsvp_that_method_save_returns_error_if_db_save_not_successful(self):
        """Test API returns error if there was a problem saving new question to db """
        # First, create a meetup record
        res_meetup = self.client.post(
            'api/v1/meetups',
            data=json.dumps({
                "topic": "RSVP the Meet",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]

        # Next, test the make rsvp endpoint
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup['id']),
            data = json.dumps({
                "meetup": meetup['id'],
                "user": 1,
                "response": 'maybe'
            }),
            content_type='application/json'
        )
        expected_output = {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

        if 'error' in res.json:
            self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
            self.assertEqual(res.status_code, 503, '503 status code not returned')

    def test_endpoint_make_rsvp_creates_rsvp_and_returns_created_rsvp(self):
        """Test API can create a rsvp and returns the created rsvp (POST request)"""
        # First, create a meetup record
        res_meetup = self.client.post(
            'api/v1/meetups',
            data=json.dumps({
                "topic": "RSVP the Meet",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]

        # Next, test the make rsvp endpoint
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup['id']), 
            data = json.dumps({
                "meetup": meetup['id'],
                "user": 1,
                "response": 'maybe'
            }),
            content_type='application/json'
        )
        expected_output = {
            "status": 201,
            "data": [
                {
                    "meetup": meetup['id'], 
                    "topic": meetup['topic'],
                    "status": "maybe"
                }
            ]
        }

        self.assertEqual(res.json['status'], expected_output['status'])
        self.assertTrue(all(item in res.json['data'][0].items() for item in expected_output['data'][0].items()))
        self.assertEqual(res.status_code, 201)

    def test_endpoint_make_rsvp_returns_error_if_meetup_id_not_exist(self):
        """Test API endpoint returns a json response"""
        meetup_id = 100
        res = self.client.post(
            'api/v1/meetups/{}/rsvps'.format(meetup_id),
            data = json.dumps({
                "meetup": "Q1 Meetup",
                "user": 'Test user',
                "response": "Yes | No | Maybe"
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

    def test_endpoint_make_rsvp_returns_error_if_route_param_invalid(self):
        """Test API returns an error if the route param is invalid (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 400,
            "error": 'Invalid route parameter'
        }

        # Next, test the make rsvp endpoint
        res = self.client.post('api/v1/meetups/invalid_param/rsvps')

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)

    def test_endpoint_fetch_meetup_returns_json(self):
        """Test API endpoint returns a json response (GET request)"""
        # First, create a meetup record
        meetup_id = 1
        res_meetup = self.client.get(
            'api/v1/meetups/{}'.format(meetup_id),
            data=json.dumps({
                "topic": "RSVP the Meet",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]
        
        res = self.client.get(
            'api/v1/meetups/{}'.format(meetup['id'])
        )       

        self.assertTrue(res.is_json)
    
    def test_endpoint_fetch_meetup_returns_specified_record(self):
        """Test API endpoint returns the specified record (GET request)"""
        # First, create a meetup record
        res_meetup = self.client.post(
            'api/v1/meetups',
            data=json.dumps({
                "topic": "Return Me",
                "location": "Nairobi",
                "happeningOn": "17/01/2019",
                "tags": []
            }),
            content_type='application/json'
        )
        meetup = res_meetup.json['data'][0]

        # Next, test fetch meetup endpoint        
        res = self.client.get(
            'api/v1/meetups/{}'.format(meetup['id'])
        )       


        self.assertTrue(all(item in res.json['data'][0].items() for item in meetup.items()))
        self.assertEqual(res.status_code, 200)
        
    def test_endpoint_fetch_meetup_returns_error_if_meetup_record_not_found(self):
        """Test API endpoint returns an error if meetup not found"""
        
        meetup_id = 100
        res = self.client.get('api/v1/meetups/{}'.format(meetup_id))

        expected_output = {
            "status": 404,
            "error": "No record found for id {}".format(meetup_id)
        }
        # pdb.set_trace()
        self.assertTrue(
            all(item in res.json.items() for item in expected_output.items()),
            'Output received does not match output expected'
        )
        self.assertEqual(res.status_code, 404)

    def test_endpoint_fetch_meetup_returns_error_if_route_param_invalid(self):
        """Test API returns an error if the route param is invalid (PATCH request)"""
        # Define the expected output
        expected_output = {
            "status": 400,
            "error": 'Invalid route parameter'
        }

        # Next, test the make rsvp endpoint
        res = self.client.get('api/v1/meetups/invalid_param')

        self.assertTrue(all(item in res.json.items() for item in expected_output.items()))
        self.assertEqual(res.status_code, 400)

    def test_endpoint_get_all_meetups_is_reachable(self):
        """Test API can fetch all upcoming meetup records (GET request)"""
        res = self.client.get('api/v1/meetups/upcoming/')       

        self.assertEqual(res.status_code, 200)
    
    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
