from flask import Blueprint

graph = Blueprint('graph', __name__, template_folder='templates', static_folder='static')

from . import index
