function get_base_route(){
	return '';
}
function album_api_route(id){
	return get_base_route() + '/api/v1/album/' + id;
}

function get_user_api_route(){
	return get_base_route() + '/api/v1/user';
}

function pic_api_route(id){
	return get_base_route() + '/api/v1/pic/' + id;
}

function static_image_route(id, format){
	return get_base_route() + '/static/images/' + id + '.' + format;
}

function pic_template_route(id){
	return get_base_route() + '/pic?id=' + id;
}

function album_template_route(id){
	return get_base_route() + '/album?id=' + id;
}
