# import pdb

import datetime

class QuestionerStorage():
    """Defines the storage class"""
    
    # static properties to be available to all instances of the class
    meetup_list = []
    rsvp_list = []
    question_list = []

    def __init__(self):
            
        self.record_new_id_not_unique = 0

    def save_item(self, list_name, item, action_type):
        
        if list_name == 'meetups':
            list_to_update = QuestionerStorage.meetup_list
        
        if list_name == 'rsvps':
            list_to_update = QuestionerStorage.rsvp_list
        
        if list_name == 'questions':
            list_to_update = QuestionerStorage.question_list

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
            'createdOn': datetime.datetime.fromtimestamp(createdOn).strftime('%d-%m-%Y')
        })
        return item
    
    def add_to_list(self, item_to_add, item_list):
        item_list.append(item_to_add)

        return item_list
    
    def get_all_records(self, list_name, criteria=''):
        if list_name == 'meetups':
            return list(self.meetup_list)
    
    def get_record(self, item_id, list_to_update):
        found_rec = []

        for item_record in list_to_update:
            if item_record['id'] == item_id:
                found_rec.append(item_record)

        if len(found_rec) == 1:
            return found_rec[0]
        elif len(found_rec) == 0:
            message = {
                "status" : 404,
                "error": "No record found for id {}".format(item_id)
            }
        else:
            message = {
                "error" : "Multiple records!"
            }
        return message

    def add_new_item_record(self, list_name, item, list_to_update):
        if self.record_new_id_not_unique > 0:
                if self.check_id_unique(self.record_new_id_not_unique, list_to_update):

                    created_on = datetime.datetime.now().timestamp()
                    new_item_record = self.set_id_and_creation_time(
                        self.record_new_id_not_unique, created_on, item
                    )
                    self.add_to_list(new_item_record, list_to_update)
                    self.record_new_id_not_unique = 0
                    # pdb.set_trace()
                    return new_item_record

                else:
                    self.add_new_item_record(list_name, item, list_to_update)

        else:
            new_id = self.generate_id(list_to_update)
            if self.check_id_unique(new_id, list_to_update):

                created_on = datetime.datetime.now().timestamp()
                new_item_record = self.set_id_and_creation_time(
                    new_id, created_on, item
                )
                self.add_to_list(new_item_record, list_to_update)
                self.record_new_id_not_unique = 0
                # pdb.set_trace()
                return new_item_record
            else:
                self.record_new_id_not_unique = self.generate_id(list_to_update)
                self.add_new_item_record(list_name, item, list_to_update)

    def update_item_record(self, item, list_to_update):
        current_idx = list_to_update.index(item)
        list_to_update.pop(current_idx)
        list_to_update.append(item)
        
        return self.get_record(item['id'], list_to_update)
