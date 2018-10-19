import os

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from app.models import House, Facility, HouseImage, Order, Area
from utils import status_code
from utils.settings import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/my_house/')
@login_required
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('/new_house/', methods=['GET', 'POST'])
@login_required
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')

    if request.method == 'POST':
        # 获取房屋信息
        house = House()
        house.user_id = current_user.id
        house.title = request.form.get('title')
        house.price = request.form.get('price')
        house.area_id = request.form.get('area_id')
        house.address = request.form.get('address')
        house.room_count = request.form.get('room_count')
        house.acreage = request.form.get('acreage')
        house.unit = request.form.get('unit')
        house.capacity = request.form.get('capacity')
        house.beds = request.form.get('beds')
        house.deposit = request.form.get('deposit')
        house.min_days = request.form.get('min_days')
        house.max_days = request.form.get('max_days')

    facilities = request.form.getlist('facility')
    for id in facilities:
        facility = Facility.query.get(id)
        house.facilities.append(facility)
    house.add_update()
    return jsonify(code=status_code.OK, house_id=house.id)


@house_blueprint.route('/house_image/', methods=['POST'])
def house_image():
    img = request.files.get('house_image')
    # 获取用户

    house_id = request.form.get('house_id')
    house = House.query.get(house_id)

    if img:
        # 保存save
        file_path = os.path.join(UPLOAD_DIR, img.filename)
        img.save(file_path)

        # 将图片保存到数据库
        house_img = HouseImage()
        house_img.house_id = house_id
        house_img.url = img.filename
        house_img.add_update()

        # 判断有无首图
        if not house.index_image_url:
            house.index_image_url = house_img.url
            house.add_update()

        # 判断房屋是否已存在
        # if house:
        #     return jsonify(status_code.HOUSE_IS_EXISTS)
        return jsonify(code=status_code.OK, img_url=house_img.url)

    else:
        return jsonify(status_code.HOUSE_IMAGE_IS_NOT_EXISTS)


@house_blueprint.route('/get_house/')
def get_house():
    houses = current_user.houses
    house_info = []
    for house in houses:
        info = house.to_dict()
        house_info.append(info)
    return jsonify(code=status_code.OK, house_info=house_info, id_name=current_user.id_name)


@house_blueprint.route('/detail/')
def detail():
    return render_template('detail.html')


@house_blueprint.route('/get_detail/<int:house_id>/')
def house_detail(house_id):
    house = House.query.get(house_id)
    house_info = house.to_full_dict()
    return jsonify(code=status_code.OK, house_info=house_info)


@house_blueprint.route('/booking/')
@login_required
def booking():
    return render_template('booking.html')


# @house_blueprint.route('/index/', methods=['GET'])
# def index():
#     return render_template('index.html')


@house_blueprint.route('/my_index/', methods=['GET'])
def my_index():
    # 获取登录用户的信息
    username = ''
    if current_user.get_id():
        username = current_user.name
    # 获取房屋的轮播图
    houses = House.query.order_by('-id').all()
    houses_info = []
    for house in houses:
        houses_info.append(house.to_dict())
    return jsonify(code=status_code.OK, username=username, houses_info=houses_info)


@house_blueprint.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blueprint.route('/my_search/', methods=['GET'])
def my_search():
    # 先获取区域id，订单开始时间，结束时间
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    # 获取某个区域的房屋信息
    houses = House.query.filter(House.area_id == aid)
    # 订单的三种情况，查询出的房屋都不能展示
    order1 = Order.query.filter(Order.end_date >= ed, Order.begin_date <= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
    order3 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    house1 = [order.house_id for order in order1]
    house2 = [order.house_id for order in order2]
    house3 = [order.house_id for order in order3]
    # 去重
    not_show_house_id = list(set(house1 + house2 + house3))
    # 最终展示的房屋信息
    houses = houses.filter(House.id.notin_(not_show_house_id))
    # 排序
    if sk == 'new':
        houses = houses.order_by('-id')
    elif sk == 'booking':
        houses = houses.order_by('-order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')

    house_info = [house.to_full_dict() for house in houses]
    return jsonify(code=status_code.OK, house_info=house_info)


@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():
    # 获取所有区域信息
    areas = Area.query.all()
    # 获取所有设施信息
    facilities = Facility.query.all()
    # 将设施和区域信息序列化
    area_info = [area.to_dict() for area in areas]
    facility_info = [facility.to_dict() for facility in facilities]
    return jsonify(code=status_code.OK, area_info=area_info,
                   facility_info=facility_info)
