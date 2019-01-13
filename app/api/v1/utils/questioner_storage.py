# import pdb

import datetime

class QuestionerStorage():
    """Defines the storage class"""
    
    def __init__(self):
        self.meetup_list = []
        self.meetup_u_n_id = 0

        self.rsvp_list = []
        self.rsvp_u_n_id = 0

    def save_item(self, list_name, item):
        if list_name == 'meetups':
            # pdb.set_trace()
            if self.meetup_u_n_id > 0:
                if self.check_id_unique(self.meetup_u_n_id, self.meetup_list):
                
                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        self.meetup_u_n_id, created_on, item
                    )
                    self.add_to_list(new_item_record, self.meetup_list)
                    self.meetup_u_n_id = 0
                    # pdb.set_trace()
                    return new_item_record
                
                else:
                    self.save_item('meetups', item)
            
            else:
                new_id = self.generate_id(self.meetup_list)
                if self.check_id_unique(new_id, self.meetup_list):

                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        new_id, created_on, item
                    )
                    self.add_to_list(new_item_record, self.meetup_list)
                    self.meetup_u_n_id = 0
                    # pdb.set_trace()
                    return new_item_record
                else:
                    self.meetup_u_n_id = self.generate_id(self.meetup_list)
                    self.save_item('meetups', item)
        elif list_name == 'rsvps':
            if self.rsvp_u_n_id > 0:
                if self.check_id_unique(self.rsvp_u_n_id, self.rsvp_list):

                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        self.rsvp_u_n_id, created_on, item
                    )
                    self.add_to_list(new_item_record, self.rsvp_list)
                    self.rsvp_u_n_id = 0
                    # pdb.set_trace()
                    return new_item_record

                else:
                    self.save_item('rsvps', item)

            else:
                new_id = self.generate_id(self.rsvp_list)
                if self.check_id_unique(new_id, self.rsvp_list):

                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        new_id, created_on, item
                    )
                    self.add_to_list(new_item_record, self.rsvp_list)
                    self.rsvp_u_n_id = 0
                    # pdb.set_trace()
                    return new_item_record
                else:
                    self.rsvp_u_n_id = self.generate_id(self.rsvp_list)
                    self.save_item('rsvps', item)


    def generate_id(self, items_list):
        item_id = 0

        item_id = len(items_list) + 1

        return item_id
    
    def increment_generated_non_unique_id(self, item_id):
        new_id = item_id + 1

        return new_id

    def check_id_unique(self, item_id, items_list):
        is_unique = False
        ids_list = []

        for item_record in items_list:
            ids_list.append(item_record['id'])
            
        if item_id in ids_list:
            is_unique = False
        else:
            is_unique = True
        
        return is_unique

    def set_id_and_creation_time(self, id_to_set, createdOn, item):
        item.update({
            'id' : id_to_set,
            'createdOn' : createdOn
        })
        return item
    
    def add_to_list(self, item_to_add, item_list):
        item_list.append(item_to_add)

        return item_list
    
    def get_all_records(self, list_name, criteria=''):
        if list_name == 'meetups':
            return list(self.meetup_list)
    
    def get_record(self, list_name, item_id):
        found_rec = []
        if list_name == 'meetups':

            for item_record in self.meetup_list:
                if item_record['id'] == item_id:
                    found_rec.append(item_record)

            if len(found_rec) == 1:
                return found_rec[0]
            elif len(found_rec) == 0:
                message = {
                    "error": "No record found for id {}".format(item_id)
                }
            else:
                message = {
                    "error" : "Multiple records!"
                }
            return message
