$(document).ready(function(){
    $(".comment-button").click(function(){
        username = $('#username').text()
        image_url = 'users/'+username+'/upload/image/'
        image_form = $('.form-horizontal').text()
        $('#form-modal-body').load(image_url)
        $('#form-modal').modal('toggle')
    });
});