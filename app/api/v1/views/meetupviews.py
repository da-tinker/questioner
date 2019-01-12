import pdb

# Define blueprint for meetup view
from flask import Blueprint, request, jsonify

from app.api.v1.models import Meetup

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
        # response = save(meetup)
        return jsonify(res_valid_data), 202
    else:
        return jsonify(res_valid_data), 202

def save(meetup):
    # do some processing

    return jsonify({
        "status": 201,
        "data": [meetup],
    }), 202

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
    
