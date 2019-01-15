def validate_request_data(request_data):
    # request_data = [  {
    #                       "required_field_1": "datatype", 
    #                       "required_field_1": "datatype"
    #                   },
    #                   {
    #                       "other_field_1" : "datatype"
    #                   }
    #               ]
    required_fields = request_data[0]
    missing_fields = []
    empty_fields = []

    for field in required_fields:
        if field not in request_data[0]:
            missing_fields.append(field)

        elif request_data[0][field] == "" or request_data[0][field] == '""':
            empty_fields.append(field)

    if len(missing_fields) > 0:
        response = {
            "status": '400',
            "error": 'Required fields missing: ' + ',  '.join(missing_fields)
        }
        return response
    elif len(empty_fields) > 0:
        response = {
            "status": '400',
            "error": 'Required field(s) empty: ' + ',  '.join(empty_fields)
        }
        return response
    else:
        non_empty = {}
        for field in request_data[1]:
            if request_data[1][field] != "" and request_data[1][field] != '""':
                non_empty.update({field : request_data[1][field]})

        return {**request_data[0], **non_empty}
