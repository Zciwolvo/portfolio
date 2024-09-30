from flask import Blueprint

gothic = Blueprint('gothic', __name__, template_folder='templates', static_folder='static')

from . import index
