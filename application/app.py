from flask import Flask
from models.db import initialize_db
from views.results import results
from views.manage import manage
import os

app = Flask(__name__)


def create_app():
    app.config['MONGODB_SETTINGS'] = {'host': os.environ.get('DB_HOST')}
    if os.environ.get('DB_HOST'):
        initialize_db(app)
    app.url_map.strict_slashes = False
    app.register_blueprint(results, url_prefix='')
    app.register_blueprint(manage, url_prefix='')


if __name__ == '__main__':
    create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
