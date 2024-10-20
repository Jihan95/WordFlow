from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JWT_SECRET_KEY'] = 'ca16e8f5b8a6e2a3b00a807e84e6117ccb075a53f1a70854f0f8022fe9f5cef1'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

USER_NAME = os.getenv('WordFlow_MYSQL_USER', 'wordflow_dev')
PWD = os.getenv('WordFlow_MYSQL_PWD', 'wordflow_dev_pwd')
HOST = 'localhost'
DB = os.getenv('WordFlow_MYSQL_DB', 'WordFlow')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER_NAME}:{PWD}@{HOST}/{DB}'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
