/**
 * Created by Dmytro on 13.05.2017.
 */
$(document).ready(function(){
    $(function(){

    $.ajax({
            type: "post",
            dataType: "html",
            url: "http://127.0.0.1:5000/api/names",
            success: function(data) {
                data = $.parseJSON(data);
               // alert(data)
               //  console.log(data)
                names = data['names']
//                console.log(names)
                for (var i = 0; i < names.length; i++) {
                    console.log( names[i] );
                    $('#currency').append('<option value="' +names[i]  + '">' +names[i] + '</option>');
                    // console.log( 'asdfghj');
                }
            }
        });
    });
});