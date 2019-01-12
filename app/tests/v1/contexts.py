import os
import sys
sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from app import create_api_server
from app.api.v1.views.meetupviews import validate_request_data
