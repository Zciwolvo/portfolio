from flask import Blueprint

portfolio = Blueprint('portfolio', __name__, template_folder='templates', static_folder='static')

from . import index
