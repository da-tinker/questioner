# Define blueprint for meetup view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import Meetup
from app.api.v1.utils import QuestionerStorage, validate_request_data, validate_route_param, invalid_param, allowed_content_types, check_is_empty

db = QuestionerStorage()

meetup_view_blueprint = Blueprint('meets', '__name__')

@meetup_view_blueprint.route('/meetups', methods=['POST'])
def create_meetup():
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
                'error' : "Request data invalid! Possibly no data supplied"
            }
            return make_response(jsonify(response), response['status'])

    # check validity of request data
    res_valid_data = meetup_validate_request_data(data)

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

def save(meetup_record):
    """Sends the meetup to be added to storage."""

    # send to storage
    db_response = db.save_item('meetups', meetup_record, 'add_new')

    if all(item in db_response.items() for item in meetup_record.items()):
        return {
            "status": 201,
            "data": [meetup_record]
        }
    else:
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def meetup_validate_request_data(req_data):
    """Validates the meetup data received"""
    # data = {
    #             "topic": "Q1 Meetup", required
    #             "location": "Nairobi", required
    #             "happeningOn": "17/01/2019", required
    #             "images": [],
    #             "Tags": [],
    #             "created_by": "User" // not mentioned in the spec doc but is logically needed
    #         }   
    #
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)

    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data    
    
    req_fields = ['topic', 'location', 'happeningOn']
    other_fields = ['images', 'tags']

    dict_req_fields = {}
    dict_other_fields = {}

    sanitized_data = []

    # get the required fields' data and put in own dictionary
    for field in req_fields:
        if field in received_data:
            dict_req_fields.update({field: received_data[field]})
    # append required fields dictionary to sanitized_data list
    sanitized_data.append(dict_req_fields)

    # get the non required fields' data and put in own dictionary
    for field in other_fields:
        if field in received_data:
            dict_other_fields.update({field: received_data[field]})
    # append non required fields dictionary to sanitized_data list
    sanitized_data.append(dict_other_fields)

    # send sanitized_data list to actual validation function and return response
    return validate_request_data(sanitized_data, req_fields)

@meetup_view_blueprint.route('/meetups/<meetup_id>', methods=['GET'])
def get_meetup(meetup_id):
    # check meetup id in route
    valid_param = validate_route_param(meetup_id)
    if type(valid_param) != int:
        return jsonify(valid_param), valid_param['status']

    # fetch meetup record
    meetup_record = db.get_record(valid_param, db.meetup_list)
    
    if 'error' in meetup_record:
        return jsonify(meetup_record), meetup_record['status']

    return jsonify({
        "status": 200,
        "data": [meetup_record]
    }), 203

@meetup_view_blueprint.route('/meetups/upcoming/', methods=['GET'])
def get_all_upcoming_meetups():
    
    meetups = db.get_all_records('meetups')

    return jsonify({
        "status": 200,
        "data": meetups
    }), 203
    
