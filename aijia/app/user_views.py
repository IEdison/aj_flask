import os
import random
import re

from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User
from utils import status_code

from utils.settings import UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)
login_manager = LoginManager()


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建表成功'


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        # 实现注册功能
        # 获取注册页面ajax提交过来的参数，request.form
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        passwd = request.form.get('passwd')
        passwd2 = request.form.get('passwd2')
        # 校验参数是否填写完整
        if not all([mobile, imagecode, passwd, passwd2]):
            return jsonify(status_code.USER_REGISTER_PARAMS_NOT_EXISTS)
        # 校验手机号
        if not re.match(r'^1[345678]\d{9}$', mobile):
            return jsonify(status_code.USER_REGISTER_PHONE_IS_NOT_VALID)
        # 校验图片验证码
        if session.get('code') != imagecode:
            return jsonify(status_code.USER_REGISTER_CODE_IS_NOT_VALID)
        # 校验密码是否一致
        if passwd != passwd2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_NOT_EQUAL)
        # 判断手机号是否注册过
        user = User.query.filter(User.phone == mobile).all()
        if user:
            return jsonify(status_code.USER_REGISTER_PHONE_IS_EXISTS)
        # 保存用户的注册信息
        user = User()
        user.phone = mobile
        # user.name = mobile
        user.password = passwd
        user.add_update()
        return jsonify(status_code.SUCCESS)


@user_blueprint.route('/img_code/', methods=['GET'])
def img_code():
    # 获取随机长度为4的验证码
    s = '1234567890qwertyuiopasdfghjklzxcvbnmm'
    code = ''
    for i in range(4):
        code += random.choice(s)
    # 将状态码code存放在session中
    session['code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # 获取手机号和密码
        mobile = request.form.get('mobile')
        passwd = request.form.get('passwd')
        # 校验参数是否完整
        if not all([mobile, passwd]):
            return jsonify(status_code.USER_LOGIN_PARAMS_NOT_EXISTS)
        # 校验手机号是否符合规格
        if not re.match(r'^1[345678]\d{9}$', mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_IS_NOT_VALID)
        # 判断手机号是否存在
        user = User.query.filter(User.phone == mobile).first()
        if not user:
            return jsonify(status_code.USER_LOGIN_IS_NOT_EXISTS)
        # 校验密码是否正确
        if not user.check_pwd(passwd):
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_NOT_VALID)
        # 记录用户登录成功
        login_user(user)
        return jsonify(status_code.SUCCESS)


@user_blueprint.route('/logout/')
def logout():
    logout_user()
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user_blueprint.route('/profile/', methods=['GET', 'PATCH'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

    if request.method == 'PATCH':
        # 获取图片
        icons = request.files.get('avatar')
        # 获取用户
        user = current_user
        if icons:
            # 保存save
            file_path = os.path.join(UPLOAD_DIR, icons.filename)
            icons.save(file_path)
            # icons_path = os.path.join('upload', icons.filename)
            user.avatar = os.path.join(icons.filename)
            user.add_update()
            return jsonify(code=status_code.OK, icons=user.avatar)

        else:
            return jsonify(status_code.USER_PROFILE_AVATAR_IS_NOT_EXISTS)


@user_blueprint.route('/show_icons/', methods=['GET'])
@login_required
def show_icons():
    user = current_user
    icons_1 = user.avatar
    return jsonify(code=status_code.OK, icons_1=icons_1)


@user_blueprint.route('/profile_name/', methods=['PATCH'])
@login_required
def profile_name():
    # 修改用户名
    # 获取用户名，校验用户名是否已经存在
    username = request.form.get('username')
    if username:
        if not User.query.filter(User.name == username).first():
            # 更新用户名
            user = current_user
            user.name = username
            user.add_update()
            return jsonify(status_code.SUCCESS)
        else:
            # 如果用户名存在，则返回错误信息
            return jsonify(status_code.USER_PROFILE_NAME_IS_EXISTS)
    return jsonify(status_code.USER_PROFILE_NAME_IS_NOT_VALID)


@user_blueprint.route('/auth/', methods=['GET', 'POST'])
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    if request.method == 'POST':
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        if not all([real_name, id_card]):
            return jsonify(status_code.USER_AUTH_PARAMS_IS_NOT_VALID)
        if re.match(r'^[1-9]\d{6}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                    id_card):
            return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)
        user = current_user
        user.id_name = real_name
        user.id_card = id_card
        user.add_update()
        return jsonify(status_code.SUCCESS)


@user_blueprint.route('/auth_info/')
def auth_info():
    user = current_user
    my_info = user.to_auth_dict()
    return jsonify(code=status_code.OK, my_info=my_info)
