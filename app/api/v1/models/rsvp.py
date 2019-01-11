import datetime

from . import BaseModel

class Rsvp(BaseModel):
    """Defines the properties specific to a Rsvp"""

    def __init__(self,
            id_= "",
            meetup = "",
            user= "",
            response="",
            created_on=datetime.date.today(),
        ):
        super().__init__(id_ = id_, created_on = created_on)
        self.meetup = meetup
        self.user = user
        self.response = response
