function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function () {

    $('#form-avatar').submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/user/profile/',
            dataType: 'json',
            type: 'PATCH',
            success: function (data) {
                if (data.code == '200') {
                    // $('#user-avatar').attr('src', '/static/media/upload/' + data.icons)
                    alert('修改成功')
                    location.href = '/user/profile/';
                }
            }
        })
    });

    $('#form-name').submit(function (e) {
        e.preventDefault();
        var username = $('#user-name').val()
        $.ajax({
            url: '/user/profile_name/',
            data: {'username': username},
            dataType: 'json',
            type: 'PATCH',
            success: function (data) {
                if (data.code == '200') {
                    alert('修改成功')
                    $('.error-msg').hide()
                }
                if (data.code == '1010') {
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }
                if (data.code == '1014'){
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }
            }
        })
    });

    $.get('/user/show_icons/', function (data) {
        if (data.code == '200') {
            $('#user-avatar').attr('src', '/static/media/upload/' + data.icons_1)
        }
    })
});
