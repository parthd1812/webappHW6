/*
@author Parth Desai
parthd@andrew.cmu.edu

*/

/*
High Level Description is as follows:
1) For the global page we have to update with any new posts every 5 sends without rehreshing the HTML page
2) The sendRequest() function sends a request to the server every 5 seconds. In the sendRequest function also sends the Primary key value of the last post
   this PK would be then used to filter out the new post and the server would then only send data related with the new post
3) The handleResponse function receives the Json data from the server. It then extracts the relevant fields from the objects
    and then uses the append/prepend methods to display it in the front end part.
4) There is also another section in this code which handles displaying the comments for a particular post with out refreshing the entier page.
   The above functionality has been implemented using the .on() method. When the "submit comment" is clicked this function gets called 
   This function then sends the "comment" and also the ID of the post to which this comments belongs to.
5) The above .on() method has been similarly implemented for the follower page and profile page. To handle comments. 
6) Concepts of event delgation have been used to handle listing to new comment forms for new post

*/

//-------------------------------Refreshing the global page every 5 sec --------------------------------------------
var req;
var lastpk;
// var comment_userid = []
// var comm =[]
//var commentdate =[]
// Function to send request
function sendRequest() {

	lastpk = $("#row_ajax div:first-child").attr("id")
	req = jQuery.get("/globalpage_ajax/", {'data':lastpk}, function(data){
		handleResponse(data)
	}
	,"json");
}
// Function to handleResponse
function handleResponse(data) {
	if (req.readyState !=4 || req.status !=200) {
		return;
	}

	var items = data;
	console.log(items);
	//Iterating over the Json objects
	for (var i = 0;  i <items.length; i++) {
    if (items[i]["model"] == "grumblr.post") {

			var post = items[i]["fields"]["text"];
			var date = items[i]["fields"]["date_time"];
			var userid = items[i]["fields"]["user"];
			var primarykey = items[i]["pk"]

			for (var j = 0; j< items.length; j++) {
				if (items[j]["model"] == "auth.user") {
					if (userid == items[j]["pk"]) {
						var username = items[j]["fields"]["username"];
					}	
				}
			}

			for (var j = 0; j < items.length; j++) {
				if (items[j]["model"] == "grumblr.document") {
					if (userid == items[j]["fields"]["user"]) {
						var image = items[j]["fields"]["docfile"];
					}
				}
			}
	  var dat = new Date(date)
      var q = 'commentblock'+primarykey
      var r = 'comment_form'+primarykey
      $('#row_ajax').prepend("\
        <div class='row' id = "+primarykey+">\
          <br>\
            <div class='col-md-3'>\
                <img src='/media/" + image + "' class='img-circle' alt='Images' width=150 height=100>\
                <br>\
                <a href ='/prof/" + username + "'> "+username+"</a>\
            </div>\
            <div class='col-md-5 date'>\
              <br>\
              <p> "+post+" </p>\
              <h6> "+dat.toLocaleString('en-US')+" </h6>\
              <div id = "+q+" ></div>\
            </div>\
            <div id = "+r+" </div>\ </div>\
         ")


			for (var j = 0; j < items.length; j++) {
				// Check if there is new comment to this new post
				if (items[j]["model"] == "grumblr.comments") {
					var comment_userid = items[j]["fields"]["user"]
					var comment_postid = items[j]["fields"]["userpost"]

					if (comment_postid == primarykey) {
						var comment_userid = items[j]["fields"]["user"]
						var comm = items[j]["fields"]["usercomment"]
						var commentdate = items[j]["fields"]["date_time"] 
					
						for (var k = 0; k < items.length; k++) {
							if (items[k]["model"] == "grumblr.document") {
								if (comment_userid == items[k]["fields"]["user"])
									var commentimage = items[k]["fields"]["docfile"]

							}
						}

						for (var l = 0 ; l <items.length; l++) {
							if (items[l]["model"] == "auth.user") {
								if(items[l]["pk"] == comment_userid) {
									var comment_username = items[l]["fields"]["username"]
								}
							}
						}
					}	
					var da = new Date(commentdate)
                    var p = ('#commentblock'+primarykey)
                    $(p). append("<div class='row post1'>\
                                            <div class = 'col-md-3'>\
                                                        <img src='/media/"+commentimage+"' class='img-circle' alt='Image' width=100 height=70>\
                                                        <a href ='/prof/" + comment_username + "'> "+comment_username+"</a>\
                                                         <br>\
                                            </div>\
                                            <div class = 'col-md-9'>\
                                                    <p>"+comm+"</p>\
                                                    <h6>"+da.toLocaleString('en-US')+"</h6>\
                                                    <br><br>\
                                            </div>\
                                        </div>")

				}
			}

			var s = ('#comment_form'+primarykey)
			var t = 'comment_'+primarykey
			$(s). append("<div class = 'col-md-4 post1'>\
                            <form class = 'new_comments' id = "+primarykey+">\
	                            <input id='id_comment' maxlength='42' name="+t+" placeholder='Add your comment here' type='text' />\
	                            <br><br>\
	                            <button type='submit'>Submit Comment</button>\
	                            <br><br>\
                            </form>\
                       </div>")
		}

	}

}
//------------------------------------------------------------------------------------------------------------------------

//---------------------------------------Adding a new Comment-------------------------------------------------------------

// .on() method with event delegation 
$(document).ready(function(){
	$("#row_ajax").on('submit','.new_comments', function(event) {
	event.preventDefault();

	var name_com = "comment_"+this.id
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
	 	console.log(responseText)
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

	 	var da = new Date(comm_date);
	 	$('#' +blockid).append("\
	                            <div class='row post1'>\
	                                <div class = 'col-md-3 post1'>\
	                                    <img src='/media/"+comm_image+"' class='img-circle' alt='Image' width=100 height=70>\
	                                    <br>\
	                                    <a href ='/prof/" + comm_user + "'> "+comm_user+"</a>\
	                                    \
	                                </div>\
	                                <div class = 'col-md-9'>\
	                                    <p>"+new_comm+"</p>\
	                                    <h6>"+da.toLocaleString()+"</h6>\
	                                    <br>\
	                                </div>\
	                            </div>\
	                            <br><br>")						    		
	 })

});
	window.setInterval(sendRequest, 5000);

  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
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
});
//----------------------------------------------END of CODE -------------------------------------------------------



