from _datetime import datetime

from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user

from app.models import House, Order
from utils import status_code

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/my_order/', methods=['POST'])
@login_required
def my_order():
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')

    # 获取当前用户和房屋id
    user_id = current_user.id
    house_id = request.form.get('house_id')
    # 获取房屋对象
    house = House.query.get(house_id)

    if house.user_id == user_id:
        return jsonify(status_code.USER_HOUSE_IS_NOT_SAME)
    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.amount = order.days * house.price
    order.house_price = house.price
    order.add_update()
    return jsonify(status_code.SUCCESS)


@order_blueprint.route('/orders/', methods=['GET'])
@login_required
def orders():
    return render_template('orders.html')


@order_blueprint.route('/orders_info/')
@login_required
def orders_info():
    # 拿到用户的所有订单信息
    orders = current_user.orders
    # 创建返回给页面的列表
    orders_info = []
    # 循环遍历所有的订单并添加到orders_info
    for order in orders:
        order_info = order.to_dict()
        orders_info.append(order_info)
    return jsonify(code=status_code.OK, orders_info=orders_info)


@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


@order_blueprint.route('/lorder_info/', methods=['GET'])
@login_required
def lorder_info():
    houses = current_user.houses
    house_ids = []
    for house in houses:
        house_ids.append(house.id)

    orders = Order.query.filter(Order.house_id.in_(house_ids))
    lorder_info = []
    for order in orders:
        order_info = order.to_dict()
        lorder_info.append(order_info)
    return jsonify(code=status_code.OK, lorder_info=lorder_info)


@order_blueprint.route('/change_status/', methods=['POST'])
@login_required
def change_status():
    # 获取页面传递信息
    order_id = request.form.get('order_id')
    comment = request.form.get('comment')
    status = request.form.get('status')
    # 获取订单
    order = Order.query.get(order_id)
    # 改变订单信息
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify(status_code.SUCCESS)