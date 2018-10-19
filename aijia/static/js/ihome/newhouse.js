function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){

    $.get('/house/area_facility/', function(data){
        if(data.code == '200'){
            for(var i=0;i<data.area_info.length; i++){
                var option_str = '<option value="'
                option_str += data.area_info[i].id + '">'
                option_str += data.area_info[i].name + '</option>'
                $('#area-id').append(option_str)
            }
            for(var j=0; j<data.facility_info.length; j++){
                var facility_str = '<li><div class="checkbox"><label>'
                facility_str += '<input type="checkbox" name="facility" value="' + data.facility_info[j].id + '">' + data.facility_info[j].name
                facility_str += '</label></div></li>'
                $('.house-facility-list').append(facility_str)
            }
        }
    });

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/new_house/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    alert('发布成功')
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                    $('#house-id').val(data.house_id)
                }
                if (data.code == '2001'){
                    alert('不能对自己的房源下单')
                }
            }
        })
    });

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/house_image/',
            dataType:'json',
            type:'POST',
            success: function(data){
                if (data.code == '200'){
                    var img = '<img src="/static/media/upload/' + data.img_url + '">'
                    $('.house-image-cons').append(img)
                }
                if (data.code == '1016'){
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }

            }
        })
    })
})