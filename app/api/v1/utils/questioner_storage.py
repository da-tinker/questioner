# import pdb

import datetime

class QuestionerStorage():
    """Defines the storage class"""
    
    def __init__(self):
        self.meetup_list = []
        self.rsvp_list = []
        self.question_list = []
        
        self.record_u_n_id = 0

    def save_item(self, list_name, item, action_type):
        
        if list_name == 'meetups':
            list_to_update = self.meetup_list
        
        if list_name == 'rsvps':
            list_to_update = self.rsvp_list
        
        if list_name == 'questions':
            list_to_update = self.question_list

        if action_type == 'add_new':
            return self.add_new_item_record(list_name, item, list_to_update)
        elif action_type == 'update':
            return self.update_item_record(item, list_to_update)

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
    
    def get_record(self, item_id, current_list):
        found_rec = []

        for item_record in current_list:
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

    def add_new_item_record(self, list_name, item, current_list):
        if self.record_u_n_id > 0:
                if self.check_id_unique(self.record_u_n_id, current_list):

                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        self.record_u_n_id, created_on, item
                    )
                    self.add_to_list(new_item_record, current_list)
                    self.record_u_n_id = 0
                    # pdb.set_trace()
                    return new_item_record

                else:
                    self.add_new_item_record(list_name, item, current_list)

        else:
            new_id = self.generate_id(current_list)
            if self.check_id_unique(new_id, current_list):

                created_on = datetime.datetime.now().timestamp()
                new_item_record = self.set_id_and_creation_time(
                    new_id, created_on, item
                )
                self.add_to_list(new_item_record, current_list)
                self.record_u_n_id = 0
                # pdb.set_trace()
                return new_item_record
            else:
                self.record_u_n_id = self.generate_id(current_list)
                self.add_new_item_record(list_name, item, current_list)

    def update_item_record(self, item, current_list):
        current_idx = current_list.index(item)
        current_list.pop(current_idx)
        current_list.append(item)
        
        return self.get_record(item['id'], current_list)
