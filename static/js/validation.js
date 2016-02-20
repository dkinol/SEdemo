function getSecret(){
	return "";
}

function displayErrors(errors){
		var result = JSON.parse(errors.responseText);
		var server_err = [];
		if ('errors' in result){
			for (i = 0; i < result.errors.length; ++i){
				server_err.push(result.errors[i].message);
			}
		}
	for (i = 0; i < server_err; ++i){
		$("#error_list").append("<li><p class=error>" + server_err[i] + "</p></li>");
	}
}

function validateEmail(email, errors){
	var re = /[^@]+@[^@]+\.[^@]+/;
	if (re.test(email) == false){
		errors.push("Email address must be valid");
	}
	if (email.length > 40){
		errors.push("Email must be no longer than 40 characters");
	}
}

function validatePassword(password1, password2, errors){
	if (password1 !== password2){
		errors.push("Passwords do not match");
	}
	var re = /^[A-Za-z0-9_]*$/;
	if (re.test(password1) == false){
		errors.push("Passwords may only contain letters, digits, and underscores");
	}
	re = /^(?=.*[a-zA-Z])(?=.*\d).+$/;
	if (re.test(password1) == false){
		errors.push("Passwords must contain at least one letter and one number");
	}
	if (password1.length < 8){
		errors.push("Passwords must be at least 8 characters long");
	}
}

function validateFirstname(firstname, errors){
	if (firstname.length > 20){
		errors.push("Firstname must be no longer than 20 characters");
	}
}

function validateLastname(lastname, errors){
	if (lastname.length > 20){
		errors.push("Lastname must be no longer than 20 characters");
	}
}

function validateUsername(username, errors){
	var re = /^[A-Za-z0-9_]*$/;
	if (re.test(username) == false){
		errors.push("Usernames may only contain letters, digits, and underscores");
	}
	if (username.length < 3){
		errros.push("Usernames must be at least 3 characters long");
	}
	if (username.length > 20){
		errors.push("Username must be no longer than 20 characters");
	}
}
