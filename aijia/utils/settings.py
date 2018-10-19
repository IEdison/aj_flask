import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# css路径
CSS_DIR = os.path.join(STATIC_DIR, 'css')

# js路径
JS_DIR = os.path.join(STATIC_DIR, 'js')

# image路径
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')

# plugins路径
PLUGINS_DIR = os.path.join(STATIC_DIR, 'plugins')

# media路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')

# upload路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')

MYSQL_DATABASES = {
    'DRIVER': 'mysql',
    'DH': 'pymysql',
    'ROOT': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'NAME': 'aijia'

}
