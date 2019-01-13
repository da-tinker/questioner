# import pdb

# Define blueprint for meetup view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import Meetup
from app.api.v1.utils import QuestionerStorage

db = QuestionerStorage()

meetup_view_blueprint = Blueprint('meets', '__name__')

@meetup_view_blueprint.route('/meetups', methods=['POST'])
def create_meetup():
    # pdb.set_trace()
    if request.content_type == 'application/x-www-form-urlencoded':
        raw_data = request.args
        data = raw_data.to_dict()

    res_valid_data = validate_request_data(data)

    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
        return make_response(jsonify(response), 202)
    else:
        return make_response(jsonify(res_valid_data), 202)

def save(meetup_record):
    # do some processing
    db_response = db.save_item('meetups', meetup_record)

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


def validate_request_data(req_data):
    # data = {
    #             "topic": "Q1 Meetup", required
    #             "location": "Nairobi", required
    #             "happeningOn": "17/01/2019", required
    #             "images": [],
    #             "Tags": [],
    #             "created_by": "User" // required
    #         }
    
    req_fields = ['topic', 'location', 'happeningOn', 'created_by']
    missing_fields = []
    empty_fields = []
    # pdb.set_trace()
    for field in req_fields:
        if field not in req_data:
            missing_fields.append(field)
        
        elif req_data[field] == "" or req_data[field] == '""':
            # pdb.set_trace()
            empty_fields.append(field)

    if len(missing_fields) > 0:
        response = {
            "status" : '400',
            "error": 'Required fields missing: ' + ',  '.join(missing_fields)
        }
        # pdb.set_trace()
        return response
    elif len(empty_fields) > 0:
        response = {
            "status": '400',
            "error": 'Required field(s) empty: ' + ',  '.join(empty_fields)
        }
        # pdb.set_trace()
        return response
    else:
        return req_data

@meetup_view_blueprint.route('/meetups/<meetup_id>', methods=['GET'])
def get_meetup(meetup_id):
    # the plan
    # pass call to storage to
    # return a meetup of specified id

    return jsonify({
        "status": 200,
        "data": [{
            "id": "",
            "topic": "",
            "location": "",
            "happeningOn": "",
            "tags":[]
        }]
    }), 203

@meetup_view_blueprint.route('/meetups/upcoming/', methods=['GET'])
def get_all_upcoming_meetups():
    # the plan
    # pass call to storage to
    # return all meetups

    return jsonify({
        "status": 200,
        "data": [{
            "id": "",
            "topic": "",
            "location": "",
            "happeningOn": "",
            "tags":[]
        }]
    }), 203
    
