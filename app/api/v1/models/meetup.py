import datetime

from . import BaseModel

class Meetup(BaseModel):
    """Defines the properties specific to a Meetup"""

    def __init__(self,
            id_= "",
            location = "",
            images = [],
            topic = "",
            happening_on = "",
            tags = [],
            created_by = "",
            created_on = datetime.date.today(),
        ):
        super().__init__(id_ = id_, created_on = created_on)
        self.topic = topic
        self.happening_on = happening_on
        self.tags = tags
        self.location = location
        self.images = images
        self.created_by = created_by
