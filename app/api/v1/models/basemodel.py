from datetime import date

class BaseModel(object):
    """Contains properties shared accorss all the models"""

    def __init__(self, id_ = "", created_on = date.today()):
        self.id = id_
        self.created_on = created_on
