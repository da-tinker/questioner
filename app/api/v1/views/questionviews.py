# Define blueprint for Question view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import Question
from app.api.v1.utils import QuestionerStorage, validate_request_data, validate_route_param, invalid_param, allowed_content_types, check_is_empty

db = QuestionerStorage()

question_view_blueprint = Blueprint('question_bps', '__name__')

@question_view_blueprint.route('/questions', methods=['POST'])
def create_question():
    response = {}
    data = {}

    # Get request data
    if request.content_type not in allowed_content_types:
        response = {
            'status': 400,
            'error': 'Invalid Content_Type request header'
        }
        return make_response(jsonify(response), response['status'])
    elif request.args:
        raw_data = request.args
        data = raw_data.to_dict()
    else:
        # content-type is ok and no url data has been set, try for json data present
        # if content-type is application/json but no data is supplied
        # then the exception will be raised otherwise if the content-type is
        # 'application/x-www-form-urlencoded' but no data is supplied
        # then the exception will not be raised
        try:
            data = request.json
        except:
            response = {
                'status': 400,
                'error': "Request data invalid! Possibly no data supplied"
            }
            return make_response(jsonify(response), response['status'])

    # check validity of request data
    res_valid_data = question_validate_request_data(data)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
        return make_response(jsonify(response), 202)
    else:
        # request data is invalid
        if 'error' in res_valid_data:
            # some required fields are not present or are empty
            return make_response(jsonify(res_valid_data), res_valid_data['status'])
        else:
            # invalid parameters present in request data
            # get the invalid parameters and return
            response = invalid_param(data, res_valid_data)

            return make_response(jsonify(response), response['status'])

def save(question_record):
    """Sends the question to be added to storage."""

    # send to storage
    db_response = db.save_item('questions', question_record, 'add_new')

    if all(item in db_response.items() for item in question_record.items()):
        return {
            "status": 201,
            "data": [question_record]
        }
    else:
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def question_validate_request_data(req_data):
    """Validates the question data received"""
    # data = {
    #             "createdBy": 0, Integer
    #             "meetup": 0, Integer
    #             "title": "", String
    #             "body": "", String
    #             "votes": 0, Integer
    #         }
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)

    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data
    
    req_fields = ['createdBy', 'meetup', 'title']
    other_fields = ['body', 'votes']

    dict_req_fields = {}
    dict_other_fields = {}

    sanitized_data = []

    # get the required fields' data and put in own dictionary
    for field in req_fields:
        if field in req_data:
            dict_req_fields.update({field: req_data[field]})    
    # append required fields dictionary to sanitized_data list
    sanitized_data.append(dict_req_fields)

    # get the non required fields' data and put in own dictionary
    for field in other_fields:
        if field in req_data:
            dict_other_fields.update({field: req_data[field]})
    # append non required fields dictionary to sanitized_data list
    sanitized_data.append(dict_other_fields)

    # send sanitized_data list to actual validation function and return response
    return validate_request_data(sanitized_data, req_fields)

@question_view_blueprint.route('/questions/<question_id>/upvote', methods=['PATCH'])
def upvote_question(question_id):

    # check id in route 
    valid_id = validate_route_param(question_id)
    if type(valid_id) != int:
        return jsonify(valid_id), valid_id['status']

    # fetch record with validated id
    question_record = db.get_record(valid_id, db.question_list)
    if 'error' not in question_record:
        # check if we have the votes key, if not, create one
        if 'votes' not in question_record:
            question_record.update({
                'votes': 0
            })
        votes = int(question_record['votes'])
        votes += 1
        question_record['votes'] = votes

        response = db.save_item('questions', question_record, 'update')

        return jsonify({
            "status": 201,
            "data": [response]
        }), 202
    else:
        return jsonify(question_record), question_record['status']

@question_view_blueprint.route('/questions/<question_id>/downvote', methods=['PATCH'])
def downvote_question(question_id):
    # check id in route
    valid_id = validate_route_param(question_id)
    if type(valid_id) != int:
        return jsonify(valid_id), valid_id['status']

    # fetch record with validated id
    question_record = db.get_record(valid_id, db.question_list)
    if 'error' not in question_record:
        # check if we have the votes key, if not, create one
        if 'votes' not in question_record:
            question_record.update({
                'votes': 0
            })
        votes = int(question_record['votes'])
        if votes > 0:
            votes -= 1
            question_record['votes'] = votes

            response = db.save_item('questions', question_record, 'update')

            return jsonify({
                "status": 201,
                "data": [response]
            }), 202
        else:
            return jsonify({
                "status": 201,
                "data": [question_record]
            }), 202
    else:
        return jsonify(question_record), question_record['status']
