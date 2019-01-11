import datetime

from . import BaseModel

class Question(BaseModel):
    """Defines the properties specific to a Question"""

    def __init__(self,
            id_= "",
            meetup = "",
            title=[],
            body = "",
            votes = "",
            created_by = "",
            created_on = datetime.date.today(),
        ):
        super().__init__(id_ = id_, created_on = created_on)
        self.meetup = meetup
        self.title = title
        self.body = body
        self.votes = votes
        self.created_by = created_by
