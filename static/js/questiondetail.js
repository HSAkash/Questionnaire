var working = false;
var start = 1;
var delete_url = '';
$(document).ready(function() {

	$.ajax({
			type: "GET",
			url: questiondetail_url,
			processData: false,
			contentType: "application/json",
			data: '',
			headers: {
				'Authorization': token
				},
			success: function(r) {
				$('#container').append(
					`<div class="content">
						<div class="user-info">
							<img src="${r['img_url']}" />
							<span>${r['username']}</span>
						</div>

						<h3>${r['title']}</h3>
						<p class="text">${r.description}</p>
						<a href="#">Edit</a>
						<a id="deletedraft" href="#">Delete</a>
						<a id="deleteconfirm" style="display:none" href="#">Confirm</a>
						<a id="deletecancle" style="display:none" href="#">Cancle</a>
					</div>

					`
				)
				$('#container').append(
					`<div class="content">
						<h3 id="answer-count">Answers: ${r.total_answer}</h3>
						<a  id="answer-give" href="${giveanswer_url}" class="btn">
							<span></span>
							<span></span>
							<span></span>
							<span></span>
							Give the Answer
						</a>
					</div>`
				)
				delete_url = r.detail_url;
			},
			error: function(r) {
					console.log("Something went wrong!");
			}
	});

	'delete confirm'
	$('#deletedraft').click(function() {
		$('#deleteconfirm').show();
		$('#deletecancle').show();
		$('#deletedraft').hide();
	});
	$('#deletecancle').click(function() {
		$('#deleteconfirm').hide();
		$('#deletecancle').hide();
		$('#deletedraft').show();
	});
	$('#deleteconfirm').click(function() {
		$.ajax({
			type: "DELETE",
			url: delete_url,
			processData: false,
			contentType: "application/json",
			data: '',
			headers: {
			  'Authorization': token
			},
			success: function(r) {
			  window.location.href = "{% url 'post:postlist' %}";
			},
			error: function(r) {
				console.log("Something went wrong!");
			}
		});
	});


	`answer`
	$.ajax({
		type: "GET",
		url: `${answerlist_url}?page=${start}`,
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
							<div class="user-info">
								<img src="${r['results'][i]['img_url']}" />
								<a style='text-decoration:none' href="${r['results'][i].detail_url}">
								<span>${r['results'][i]['username']}</span></a>
							</div>

							<p class="text">${r['results'][i].description}</p>
							<a href="#">Edit</a>
							<a href="#">Delete</a>
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


	$(window).scroll(function() {
		if ($(this).scrollTop() + 1 >= $('body').height() - $(window).height()) {
			if (working == false) {
				working = true;
				`answer`
				$.ajax({
					type: "GET",
					url:  `${answerlist_url}?page=${start}`,
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
										<div class="user-info">
											<img src="${r['results'][i]['img_url']}" />
											<a style='text-decoration:none' href="${r['results'][i].detail_url}">
											<span>${r['results'][i]['username']}</span></a>
										</div>
	
										<p class="text">${r['results'][i].description}</p>
										<a href="#">Edit</a>
										<a href="#">Delete</a>
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
			}
		}
	})


}) // end of document.ready

