from flask import Blueprint

skapiec = Blueprint('skapiec', __name__, template_folder='templates', static_folder='static')

from . import index
