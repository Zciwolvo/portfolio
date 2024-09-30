from flask import Blueprint

warhammer = Blueprint('warhammer', __name__, template_folder='templates', static_folder='static')

from . import index
