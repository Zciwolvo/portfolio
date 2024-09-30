from flask import Blueprint

dipoe = Blueprint('dipoe', __name__, template_folder='templates', static_folder='static')


from . import index
