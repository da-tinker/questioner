# Define blueprint for rsvp view
from flask import Blueprint, request, jsonify

from app.api.v1.models import rsvp

rsvp_view_blueprint = Blueprint('rsvp_bp', '__name__')


@rsvp_view_blueprint.route('/meetups/<meetup_id>/rsvps', methods=['POST'])
def create_rsvp(meetup_id):
    # the plan:
    # get the request data then
    # save as json object
    # then return success message
    data = request.get_json()
    
    if data:
        # extract rsvp info
        pass
    else:
        rsvp = {"error": "no data"}

    # save rsvp data and return
    response = save(rsvp)


    # To-Do: check that response is of correct structure
    return response

def save(rsvp):
    # do some processing
    
    return jsonify({
        "status": 201,
        "data": [rsvp],
    }), 202
