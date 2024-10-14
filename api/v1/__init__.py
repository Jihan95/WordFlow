from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

USER_NAME = os.getenv('WordFlow_MYSQL_USER', 'wordflow_dev')
PWD = os.getenv('WordFlow_MYSQL_PWD', 'wordflow_dev_pwd')
HOST = 'localhost'
DB = os.getenv('WordFlow_MYSQL_DB', 'WordFlow')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER_NAME}:{PWD}@{HOST}/{DB}'

bcrypt = Bcrypt(app)
