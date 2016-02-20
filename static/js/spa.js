save_state = true;
function AppState(intype, inid){
	this.type = intype;
	this.id = inid;
}

var AlbumId = -1;
// Sets the basic page contents for an album
function set_album_context(albumid){
		$("#content").empty();
		AlbumId = albumid;
		$("#content").append("<h1>This is a view for a single album, a user cannot edit</h1>");
		$("#content").append("<h2 id=album_title class=text-center></h2>");
		$("#content").append("<ul id=album_list></ul>");
}

// Sets the basic page contents for a picture
function set_pic_context(picid){
	$("#content").empty();
	$("#content").append('<img id=full_pic />'); 
	$("#content").append('<p id=pic_' + picid+ '_caption />');
	$("#content").append('<a id=prev_pic />');
	$("#content").append('<a id=parent_album />'); 
	$("#content").append('<a id=next_pic />');
} 

// Thumbnail templage for a picture in /album
function thumb_pic_template(picid, picformat){
	return '<div class=row>' + 
		'<a id=pic_' + picid + '_link class="btn btn-primary" target=' + picid + '>View</a>' +
		'<img src="' + static_image_route(picid, picformat) + '" width=128 height=128></div>';
}

// Function meant for displaying an album
function displayAlbum(album){
	$("#album_title").val(album.title);
	for (i = 0; i < album.pics.length; ++i){
		var new_ele = thumb_pic_template(album.pics[i].picid, album.pics[i].format);
		$("#album_list").append("<li>Picture: " + new_ele + "</li>");
	}
}

// Fetches and displays album from server
function get_and_display_album(albumid){
	AlbumId = albumid;
	$.ajax({
		url: album_api_route(albumid),
		type: "GET",
		success: function(result){
			var Album = result;
			if (save_state){
				console.log("Save album state");
				var app_state = new AppState('album', albumid);
				history.pushState(app_state, "", album_template_route(AlbumId));
				console.log(app_state);
			}
			displayAlbum(Album);
			save_state = true;
		},
		error: function(error_resp){
			displayErrors(error_resp);
			$("#content").empty();
		}
	});
}

// Represents a model for a picture
var PicModel = {
	albumid: "",
	caption: "",
	format: "",
	next: "",
	picid: "",
	prev: ""
};

/// Templating functions for pictures
function full_pic_template(src){
	return '<img src="'+src+'" style="width:100%;height=100%;" alt="" />'; 
}
function comment_template(pic_id, pic_comment){
	return '<p class="text-center" id="'+pic_id+'" >'+pic_comment+'</p>'; 
}
function prev_pic_template(pic_url, picid){
	return '<a id="prev_pic" type="button" class="btn btn-default" href="'+pic_url+'" target="' + picid + '">Previous</a>'; 
}
function parent_album_template(album_url){
	return '<a id="parent_album" type="button" class="btn btn-default" href="'+album_url+'">Return to Album</a>';
}
function next_pic_template(pic_url, picid){
	return '<a id="next_pic" type="button" class="btn btn-default" href="'+pic_url+'" target="' + picid + '">Next</a>'; 
}

// Function takes a picture and displays it
function displayPicture(photo){
	$("#content").empty();
	$("#content").append(full_pic_template(static_image_route(photo.picid, photo.format)));
	$("#content").append(comment_template("pic_"+photo.picid+"_caption", photo.caption));
	if (photo.prev != ""){
		$("#content").append(prev_pic_template(pic_template_route(photo.prev), photo.prev));
	}
	$("#content").append(parent_album_template(album_template_route(photo.albumid)));
	if (photo.next != "") {
		$("#content").append(next_pic_template(pic_template_route(photo.next), photo.next)); 
	}
}

// Function gets picture from server then displays it
function get_and_display_pic(inpicid){
	$.ajax({
		url: pic_api_route(inpicid), 
		type: "GET", 
		success: function(result) {
			PicModel = result; 
			if (save_state === true){
				console.log("Save pic state");
				var app_state = new AppState("pic", PicModel.picid);
				console.log(app_state);
				history.pushState(app_state, "", pic_template_route(PicModel.picid));
			}
			displayPicture(PicModel); 
			save_state = true;
		},
		error: function(error_resp){
			displayErrors(error_resp);
			$("#content").empty()
		}
	}); 
}

window.onpopstate = function(event){
	save_state = false;
	if ('state' in event){
		if (event.state != null){
			if (event.state.type == 'album'){
				set_album_context(event.state.id);
				get_and_display_album(event.state.id);
			}
			else if (event.state.type == 'pic'){
				set_pic_context(event.state.id);
				get_and_display_pic(event.state.id);
			}
		}
	}
}

// Album page, when clicked it loads a picture
$('body').on('click', "a[id^='pic_']", function(event){
		// Prevents the user from following the link
		event.preventDefault();
		var picId = event.target.target;
		//var app_state = new AppState("album", AlbumId);
		//history.pushState(app_state, "", album_template_route(AlbumId));
		set_pic_context(picId);
		get_and_display_pic(picId);
});

// Controller functions for next and previous pic
$('body').on('click', "#prev_pic", function(event){
	event.preventDefault();
	var picid = event.target.target;
	//var app_state = new AppState("pic", PicModel.picid);
	//history.pushState(app_state, "", pic_template_route(PicModel.picid));
	get_and_display_pic(picid);
});

$('body').on('click', "#next_pic", function(event){
	event.preventDefault();
	var picid = event.target.target;
	//var app_state = new AppState("pic", PicModel.picid);
	//history.pushState(app_state, "", pic_template_route(PicModel.picid));
	get_and_display_pic(picid);
});

$('body').on('click', "#parent_album", function(event){
	event.preventDefault();
	//var app_state = new AppState("pic", PicModel.picid);
	//history.pushState(app_state, "", pic_template_route(PicModel.picid));
	set_album_context();
	get_and_display_album(PicModel.albumid);
});

// Controller function for editing caption
$("#new_cap").submit(function(event){
	// Prevents the form from submitting normally
	event.preventDefault();
	PicModel.caption = $("#pic_caption_input").val();
	$.ajax({
		url: pic_api_route(PicModel.picid),
		type: 'PUT',
		contentType: "application/json",
		data: JSON.stringify(PicModel),
		success: function(response){
			console.log(response);
			$("#pic_caption_input").val("");
			$('#pic_' + PicModel.picid + '_caption').val(PicModel.caption);
		},
		error: function(error_resp){
			displayErrors(error_resp);
		}
	});
});
