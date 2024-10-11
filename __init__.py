from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

USER_NAME = os.getenv('WordFlow_MYSQL_USER', 'wordflow_dev')
PWD = os.getenv('WordFlow_MYSQL_PWD', 'wordflow_dev_pwd')
HOST = 'localhost'
DB = os.getenv('WordFlow_MYSQL_DB', 'WordFlow')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER_NAME}:{PWD}@{HOST}/{DB}'

bcrypt = Bcrypt(app)
