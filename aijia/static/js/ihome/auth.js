function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $('#form-auth').submit(function (e) {
        e.preventDefault();
        $('#real-name').focus(function () {
            $('.error-msg').hide()
        })
        $('#id-card').focus(function () {
            $('.error-msg').hide()
        })
        var real_name = $('#real-name').val()
        var id_card = $('#id-card').val()
        $.ajax({
            url: '/user/auth/',
            data: {'real_name': real_name, 'id_card': id_card},
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                if (data.code == '200') {
                    alert('认证成功')
                    location.href = '/user/my/'
                }
                if (data.code == '1011' | data.code == '1012') {
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }
            }
        })
    })
    $.get('/user/auth_info/', function(data){
        if (data.code == '200'){
            $('#real-name').val(data.my_info.id_name)
            $('#id-card').val(data.my_info.id_card)
            if(data.my_info.id_name){
                $('.btn-success').hide()
            }
        }
    })
})