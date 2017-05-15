/**
 * Created by Dmytro on 13.05.2017.
 * Modified by Igor on 15.05.2017 LoLz!
 */

function getCookie (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
  };

$(document).ready(function(){
    $(function(){
    var csrf_token = getCookie('csrftoken');

    $.ajax({
            type: "get",
            url: "http://127.0.0.1:5000/api/names",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            success: function(data) {
                names = data['names'];
                for (var i = 0; i < names.length; i++) {
                    $('#currency').append('<option value="' +names[i]  + '">' +names[i] + '</option>');
                }
            }
        });
    });
});