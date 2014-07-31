$(document).ready(function(){
    $(".upload-image").click(function(){
        username = $('#username').text()
        image_url = 'users/'+username+'/upload/image/'
        $('#form-modal-body').load(image_url)
        $('#form-modal').modal('toggle')
    });
});

