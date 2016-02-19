''' This takes a list of error messages'''
def generate_error_response(errors):
    messages = []
    for error in errors:
        messages.append({'message': error})
    final_dict = {'errors': messages}
    return final_dict

