function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var search_url = location.search
    house_id = search_url.split('=')[1]
    $.get('/house/get_detail/' + house_id + '', function(data){
        // var booking_temp = template('booking_temp_script', {ohouse: data.house_info})
        // $('.house-info').html(booking_temp)
        if (data.code == '200') {
            $('.house-info-img').attr('src', '/static/media/upload/' + data.house_info.images[0])
            $('.house-text h3').html(data.house_info.title)
            $('.house-text span').html(data.house_info.price)
        }
    });

    $('.submit-btn').click(function(){
        var start_date = $('#start-date').val()
        var end_date = $('#end-date').val()
        $.ajax({
            url:'/order/my_order/',
            data:{'begin_date': start_date, 'end_date': end_date, 'house_id': house_id},
            dataType:'json',
            type:'POST',
            success:function(data){
                console.log(200)
                if(data.code == '200'){
                    location.href = '/order/orders/'
                }
            }
        })
    })
})
