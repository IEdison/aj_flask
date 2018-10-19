//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    $.get('/order/orders_info/', function (data) {
        if (data.code == '200') {
            var order_html = template('orders-list-tmpl', {orders: data.orders_info})
            $('.orders-list').html(order_html)
            $(".order-comment").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-comment").attr("order-id", orderId);
            });
            $(".order-accept").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
        }
    });

    $('.modal-accept').on('click', function () {
        var order_id = $('.modal-accept').attr('order-id')
        var status = 'COMPLETE';

        $.ajax({
            url: '/order/change_status/',
            data: {'order_id': order_id, 'status': status},
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                location.reload()
            }
        })
    });

    $('.modal-comment').on('click', function () {
        var order_id = $('.modal-comment').attr('order-id')
        var status = 'COMPLETE'
        var comment = $('#comment').val()


        $.ajax({
            url: '/order/change_status/',
            data: {'order_id': order_id, 'comment':comment, 'status':status},
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                location.reload()
            }
        })
    })
});