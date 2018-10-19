OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}

# 登陆注册模块（1000到1100）
USER_REGISTER_PARAMS_NOT_EXISTS = {'code': 1000, 'msg': '请填写完整的参数'}
USER_REGISTER_PHONE_IS_NOT_VALID = {'code': 1001, 'msg': '手机号不符合规范'}
USER_REGISTER_CODE_IS_NOT_VALID = {'code': 1002, 'msg': '图片验证码错误'}
USER_REGISTER_PASSWORD_NOT_EQUAL = {'code': 1003, 'msg': '密码不一致'}
USER_REGISTER_PHONE_IS_EXISTS = {'code': 1004, 'msg': '该手机号已注册，请去登陆'}

USER_LOGIN_PARAMS_NOT_EXISTS = {'code': 1005, 'msg': '请填写完整的参数'}
USER_LOGIN_PHONE_IS_NOT_VALID = {'code': 1006, 'msg': '登陆手机号不符合规范'}
USER_LOGIN_IS_NOT_EXISTS = {'code': 1007, 'msg': '登陆用户不存在，请去注册'}
USER_LOGIN_PASSWORD_IS_NOT_VALID = {'code': 1008, 'msg': '登陆密码不正确'}

USER_PROFILE_AVATAR_IS_NOT_EXISTS = {'code': 1009, 'msg': '请选择用户头像'}
USER_PROFILE_NAME_IS_EXISTS = {'code': 1010, 'msg': '用户名已存在，请更换用户名'}
USER_PROFILE_NAME_IS_NOT_VALID = {'code': 1014, 'msg': '请填写用户名'}

USER_AUTH_PARAMS_IS_NOT_VALID = {'code': 1011, 'msg': '请填写完整的实名认证信息'}
USER_AUTH_ID_CARD_IS_NOT_VALID = {'code': 1012, 'msg': '请填写正确的身份证号'}

# 房屋模块
USER_AUTH_NOT_VALID = {'code': 1013, 'msg': '用户没实名认证'}

HOUSE_IMAGE_IS_NOT_EXISTS = {'code': 1015, 'msg': '请选择房屋图片'}

HOUSE_IS_EXISTS = {'code': 1016, 'msg': '房源已存在'}

# 订单模块
USER_HOUSE_IS_NOT_SAME = {'code': 2001, 'msg': '不能对自己的房源下单'}
