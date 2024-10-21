from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.users import *  # type: ignore
from api.v1.views.posts import *  # type: ignore
from api.v1.views.comments import *  # type: ignore
from api.v1.views.categories import *  # type: ignore