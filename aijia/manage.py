from flask import render_template
from flask_script import Manager

from utils.app import create_app

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


manage = Manager(app=app)
if __name__ == '__main__':
    manage.run()
