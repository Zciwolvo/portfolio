from flask import Blueprint

kegdelpol = Blueprint('kegdelpol', __name__, template_folder='templates', static_folder='static')

from . import index
