$(document).ready(function () {
    $.get('/house/get_house/', function (data) {
        if (data.code == '200') {
            $("#houses-list").show();
            var i = 0
            // 循环house_info得到每一个房源信息
            for (i; i < data.house_info.length; i++) {
                // 生成每一个房源的<li>标签
                var info =
                    '<li>' +
                    '<a href="/house/detail/?house_id=' + data.house_info[i].id + '"><div class="house-title"><h3>房屋ID:' + data.house_info[i].id + '————'+ data.house_info[i].title +'</h3></div><div class="house-content"><img src="/static/media/upload/' + data.house_info[i].image + '"><div class="house-text"><ul><li>位于:' + data.house_info[i].address + '</li><li>价格:￥' + data.house_info[i].price + '/晚</li><li>发布时间:' + data.house_info[i].create_time + '</li></ul></div></div></a>'
                    + '</li>';
                $('#houses-list').append(info)
            }
            if (data.id_name){
                $('#id_name_ture').hide()
            }else{
                $('#id_name_ture').show()
                $("#houses-list").hide();
            }
        }
    })
})