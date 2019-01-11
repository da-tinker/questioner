# Define blueprint for Question view
from flask import Blueprint, request, jsonify

from app.api.v1.models import Question

question_view_blueprint = Blueprint('question_bps', '__name__')


@question_view_blueprint.route('/questions', methods=['POST'])
def create_question():
    # the plan:
    # get the request data then
    # save as json object
    # then return success message
    data = request.get_json()
    
    if data:
        location = data.get('location')
        images = data.get('images')
        topic = data.get('topic')
        happeningOn = data.get('happening on')
        tags = data.get('tags')

        Question = jsonify(location, images, topic, happeningOn, tags)
    else:
        Question = {"error": "no data"}

    response = save(Question)

    return response

def save(Question):
    # do some processing

    return jsonify({
        "status": 201,
        "data": [Question],
    }), 202


@question_view_blueprint.route('/questions/<question_id>/upvote', methods=['PATCH'])
def upvote_question(question_id):
    # the plan
    # get votes from question
    # increase by 1
    # submit to storage
    # if storage ok, return
    # else return error and notification to retry later
    return jsonify({
        "status": 201,
        "data": [{
            "meetup": '',
            "title": '',
            "body": '',
            "votes": ''
        }]
    }), 202
