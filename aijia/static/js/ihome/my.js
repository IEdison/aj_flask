function logout() {
    $.get("/user/logout/", function (data) {
        if (data.code == '200') {
            location.href = "/";
        }
    })
}

$(document).ready(function () {
    $.get('/user/show_icons/', function (data) {
        if (data.code == '200') {
            $('#user-avatar').attr('src', '/static/media/upload/' + data.icons_1)
        }
    })
})