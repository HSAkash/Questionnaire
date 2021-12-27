var start = 1;
var working = false;
$(document).ready(function() {
	$.ajax({
			type: "GET",
			url: draflist_url+"?page="+start,
			processData: false,
			contentType: "application/json",
			data: '',
			headers: {
				'Authorization': token
			},
			success: function(r) {
				for (var i = 0; i < r['results'].length; i++) {
						// $('body').append("<div><h1>"+r[i].videoName+"</h1><h2>Video Views: "+r[i].videoViews+"</h2></div>")
						$('#container').append(
							`<div class="content">

								<h3>${r['results'][i]['title']}</h3>
								<p class="text">${r['results'][i].description}</p>
								<a href="${r['results'][i]['id']}/">Read More</a>
							</div>
							`
						)
				}
				start += 1;
			},
			error: function(r) {
					console.log("Something went wrong!");
			}
	});

}) // end of document.ready
$(window).scroll(function() {
		if ($(this).scrollTop() + 1 >= $('body').height() - $(window).height()) {
				if (working == false) {
						working = true;
						$.ajax({
								type: "GET",
								url: draflist_url+"?page="+start,
								processData: false,
								contentType: "application/json",
								data: '',
								headers: {
									'Authorization': token
							   },
								success: function(r) {
										for (var i = 0; i <  r['results'].length; i++) {
											$('#container').append(
												`<div class="content">

													<h3>${r['results'][i]['title']}</h3>
													<p class="text">${r['results'][i].description}</p>
													<a href="${r['results'][i]['id']}">Read More</a>
												</div>
												`
											)
										}
										start += 1;
										setTimeout(function() {
												working = false;
										}, 4000)
								},
								error: function(r) {
										console.log("Something went wrong!");
								}
						});
				}
		}
})
