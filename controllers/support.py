''' This takes a list of error messages'''
def generate_error_response(errors):
    messages = []
    for error in errors:
        messages.append({'message': error})
    final_dict = {'errors': messages}
    return final_dict

def send_401():
	errors = []
	errors.append("You do not have the necessary credentials for the resource")
	return generate_error_response(errors)

def send_403():
	errors = []
	errors.append("You do not have the necessary permissions for the resource")
	return generate_error_response(errors)
