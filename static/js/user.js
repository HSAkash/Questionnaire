$('document').ready(function(){
    `Search`
    const login_url = `api/login`;
    $("#input").keyup(function (e) {
      let userData = e.target.value;
      $('#search_item').empty();
  
      if (userData.length > 0) {
        $.ajax({
            type: "GET",
            url: search_url+userData,
            processData: false,
            contentType: "application/json",
            data: '',
            headers: {
              'Authorization': token
              },
            success: function(r) {
              for (var i = 0; i < r['results'].length; i++){
                $('#search_item').append(
                  `<li><a href="${r['results'][i].detail_url}">${r['results'][i]['title']}</a></li>`
                )
              }
            },
            error: function(r) {
              console.log("Something went wrong!");
            }
        });
      }
    })
  
  })
  