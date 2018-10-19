function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    var mySwiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();

    var search_url = location.search
    house_id = search_url.split('=')[1]
    $.get('/house/get_detail/' + house_id + '/', function (data) {
        if (data.code == '200') {
            for (var i = 0; i < data.house_info.images.length; i++) {
                var swiper_li = '<li class="swiper-slide"><img src="/static/media/upload/' + data.house_info.images[i] + '"></li>'
                $('.swiper-wrapper').append(swiper_li)
            }
            var mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })

            $('.house-price span').html(data.house_info.price)
            $('.house-title').html(data.house_info.title)
            $('.landlord-pic img').attr('src' , '/static/media/upload/' + data.house_info.user_avatar + '')
            $('.landlord-name span').html(data.house_info.user_name)
            $('.house-info-add').html('地址:'+data.house_info.address)
            $('.icon-text-sum').html('出租'+data.house_info.room_count+'间')
            $('.house-area').html('房屋面积:' + data.house_info.acreage + '平米')
            $('.house-area-a').html('房屋户型:' + data.house_info.unit)
            $('.live-person').html(data.house_info.capacity)
            $('.bed-f').html(data.house_info.beds)
            $('.recv-money span').html(data.house_info.deposit)
            $('.min-days span').html(data.house_info.min_days)
            $('.max-days span').html(data.house_info.max_days)
            for (var i = 0; i < data.house_info.facilities.length;i++){
                var f_li = '<li><span class='+ data.house_info.facilities[i].css +'></span>'+ data.house_info.facilities[i].name +'</li>'
                    $('.house-facility-list').append(f_li)
            }
            $('.book-house').attr('href', '/house/booking/?house_id=' + house_id )
        }


    })
})