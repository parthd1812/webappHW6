/*
@author Parth Desai
parthd@andrew.cmu.edu

*/
//---------------------------------------Adding a new Comment-------------------------------------------------------------

$(".new_comments").on('submit', function(event) {
	event.preventDefault();
	var name_com = "comment_"+this.id
	console.log(name_com)
	console.log($("[name="+name_com+"]").val())
	var com = $.ajax ({
		url: "/comment/"+this.id,
		data: 
		{
			'comment': $("[name="+name_com+"]").val()
		},
		type: "POST",
		dataType: "json",

	});

     // Iterating over the responseText data to obtain the required fields
	 return com.done(function(responseText) {
	 	var blockid = "commentblock"+responseText[0]['fields']['userpost'];
	 	$("[name="+name_com+"]").val('')
	 	for (var i = 0; i<responseText.length; i++) {
	 		if (responseText[i]['model'] == "grumblr.comments") {
	 			var new_comm = responseText[i]['fields']['usercomment']
	 		}
	 		if (responseText[i]['model'] == "auth.user") {
	 			var comm_user = responseText[i]['fields']['username']
	 		}
	 		if (responseText[i]['model']=="grumblr.document") {
	 			var comm_image = responseText[i]['fields']['docfile']
	 		}
	 		if (responseText[i]['model'] == "grumblr.comments") {
	 			var comm_date = responseText[i]['fields']['date_time']
	 		}
	 	}
	 	var da = new Date(comm_date)
	 	$('#' + blockid).append("<div id = commentblock{{content.pk}}>\
                                    <div class='row post1'>\
                                        <div class = 'col-md-3'>\
                                            <img src='/media/"+comm_image+"' class='img-circle' alt='Image' width=100 height=70>\
                                            <a href ='/prof/" + comm_user + "'> "+comm_user+"</a>\
                                             <br>\
                                        </div>\
                                        <div class = 'col-md-9'>\
                                            <p>"+new_comm+"</p>\
                                            <h6>"+da.toLocaleString()+"</h6>\
                                            <br><br>\
                                        </div>\
                                    </div>\
                                    <br><br>\
                        		</div> ")
	 									
	 	
	 })

});

function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
 });
 //-------------------------------------End of Code----------------------------------------