# Define blueprint for rsvp view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import rsvp
from app.api.v1.utils import QuestionerStorage, validate_request_data, validate_route_param, check_is_empty, parse_request, endpoint_error_response

db = QuestionerStorage()

rsvp_view_blueprint = Blueprint('rsvp_bp', '__name__')

@rsvp_view_blueprint.route('/meetups/<meetup_id>/rsvps', methods=['POST'])
def create_rsvp(meetup_id):
    response = {}
    data = {}

    # check meetup_id in route can be converted to int
    validated_meetup_id = validate_route_param(meetup_id)
    if type(validated_meetup_id) != int:
        return jsonify(validated_meetup_id), validated_meetup_id['status']
    
    # check if meetup_id is for existing meetup     
    if is_meetup_id_invalid(validated_meetup_id):
        response = {
            "status" : 404,
            "error": "Meetup with id {} not found".format(validated_meetup_id)
        }
        return make_response(jsonify(response), response['status'])
        
    # Get request data
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])

    # perform standard validation checks
    res_valid_data = rsvp_validate_request_data(data, validated_meetup_id)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
        return make_response(jsonify(response), response['status'])
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)
        return make_response(jsonify(response), response['status'])

def save(rsvp_record):
    """Sends the rsvp to be recorded to storage."""

    # send to storage
    db_response = db.save_item('rsvps', rsvp_record, 'add_new')

    if all(item in db_response.items() for item in rsvp_record.items()):
        return {
            "status": 201,
            "data": [rsvp_record]
        }
    else:
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def is_meetup_id_invalid(meetup_id):
    """Checks whether the supplied meetup id exists\n Returns boolean"""
    exists = False
    exists = db.check_id_unique(int(meetup_id), db.meetup_list)
    return exists

def rsvp_validate_request_data(req_data, meetup_id):
    """Validates the rsvp data received"""
    # data = {
    #             "meetup": 1, required
    #             "user": 2, required
    #             "response": "yes | no | maybe", required
    #         }
    # 
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)
    # exit if indeed data is empty else check that response value is allowed
    if 'error' in received_data:
        return received_data
    # Confirm that the meetup supplied in route matches the id in request data
    elif 'meetup' in received_data:
        # check if meetup id can be parsed as an int
        try:
            parsed_meetup_id = int(received_data['meetup'])
        except:
            response = {
                "status": 400,
                "error": "Invalid meetup id: {}".format(received_data['meetup'])
            }
            return response
        else:
            # check if parsed meetup id matches the one in route
            if parsed_meetup_id != meetup_id:
                response = {
                    'status': 400,
                    'error': 'Meetup ID in request route ({}) does not match meetup id in request data ({}). i.e. {} != {} '.format(meetup_id, received_data['meetup'], meetup_id, received_data['meetup'])
                }
                return response
    # Confirm that the supplied value for response is what is expected
    if 'response' in received_data and received_data['response'] not in ['yes', 'no', 'maybe']:
        response = {
            'status': 400,
            'error': 'Invalid response. Must be one of: yes | no | maybe'
        }
        return response

    # all is ok. Perform standard validation checks
    req_fields = ['meetup', 'user', 'response']
    other_fields = []

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
