import pdb
# Define blueprint for Question view
from flask import Blueprint, request, jsonify, make_response

from app.api.v1.models import Question
from app.api.v1.utils import QuestionerStorage, validate_request_data

db = QuestionerStorage()

question_view_blueprint = Blueprint('question_bps', '__name__')

@question_view_blueprint.route('/questions', methods=['POST'])
def create_question():
    raw_data = request.args
    data = raw_data.to_dict()
    
    res_valid_data = question_validate_request_data(data)

    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
        return make_response(jsonify(response), 202)
    else:
        return make_response(jsonify(res_valid_data), 202)

def save(question_record):
    # do some processing
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
    # data = {
    #             "createdBy": 0, Integer
    #             "meetup": 0, Integer
    #             "title": "", String
    #             "body": "", String
    #             "votes": 0, Integer
    #         }
    req_fields = ['createdBy', 'meetup', 'title']
    other_fields = ['body', 'votes']

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
    # pdb.set_trace()
    return validate_request_data(sanitized_data, req_fields)

@question_view_blueprint.route('/questions/<question_id>/upvote', methods=['PATCH'])
def upvote_question(question_id):
    # pdb.set_trace()
    question_record = db.get_record(int(question_id), db.question_list)
    votes = int(question_record['votes'])
    votes += 1
    question_record['votes'] = votes

    response = db.save_item('questions', question_record, 'update')

    return jsonify({
        "status": 201,
        "data": [response]
    }), 202

@question_view_blueprint.route('/questions/<question_id>/downvote', methods=['PATCH'])
def downvote_question(question_id):
    question_record = db.get_record(int(question_id), db.question_list)
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
