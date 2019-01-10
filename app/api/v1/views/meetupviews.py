# Define blueprint for meetup view
from flask import Blueprint, request, jsonify

from app.api.v1.models import Meetup

meetup_view_blueprint = Blueprint('meets', '__name__')


@meetup_view_blueprint.route('/meetups', methods=['POST'])
def create_meetup():
    # the plan:
    # get the request data then
    # save as json object
    # then return success message
    data = request.json
    
    if data:
        location = data.get('location')
        images = data.get('images')
        topic = data.get('topic')
        happeningOn = data.get('happening on')
        tags = data.get('tags')

        meetup = jsonify(location, images, topic, happeningOn, tags)
    else:
        meetup = {"error": "no data"}

    response = save(meetup)

    return response

def save(meetup):
    # do some processing

    return jsonify({
        "status": 201,
        "data": [meetup],
    })
