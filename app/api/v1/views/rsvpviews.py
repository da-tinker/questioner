# import pdb

# Define blueprint for rsvp view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import rsvp
from app.api.v1.utils import QuestionerStorage, validate_request_data

db = QuestionerStorage()

rsvp_view_blueprint = Blueprint('rsvp_bp', '__name__')


@rsvp_view_blueprint.route('/meetups/<meetup_id>/rsvps', methods=['POST'])
def create_rsvp(meetup_id):
    # pdb.set_trace()
    # if is_meetup_id_invalid(meetup_id):
    #     response = {
    #         "status" : 404,
    #         "error": "Meetup with id {} not found".format(meetup_id)
    #     }
    #     return make_response(jsonify(response), 202)

    raw_data = request.args
    data = raw_data.to_dict()

    res_valid_data = rsvp_validate_request_data(data)

    # Ad-hoc validation for response
    if data['response'] not in ['yes', 'no', 'maybe']:
        response = {
            'status': '405',
            'error' : 'Invalid response. Must be one of: yes | no | maybe'
        }
        return make_response(jsonify(response), 202)

    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
        return make_response(jsonify(response), 202)
    else:
        return make_response(jsonify(res_valid_data), 202)

def save(rsvp_record):
    # do some processing
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
    exists = False
    m_id = int(meetup_id)
    exists = db.check_id_unique(m_id, db.meetup_list)
    # pdb.set_trace()
    return exists


def rsvp_validate_request_data(req_data):
    # data = {
    #             "meetup": 1, required
    #             "user": 2, required
    #             "response": "yes | no | maybe", required
    #         }
    req_fields = ['meetup', 'user', 'response']
    other_fields = []

    dict_req_fields = {}
    dict_other_fields = {}

    sanitized_data = []

    for field in req_fields:
        if field in req_data:
            dict_req_fields.update({field: req_data[field]})
    sanitized_data.append(dict_req_fields)

    for field in other_fields:
        if field in req_data:
            dict_other_fields.update({field: req_data[field]})
    sanitized_data.append(dict_other_fields)

    return validate_request_data(sanitized_data, req_fields)
