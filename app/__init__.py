# app/__init__.py
from flask import Flask, current_app
from dotenv import load_dotenv
import os


def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    app.config['DIPOE_USER'] = os.getenv("MAIL_USER_DIPOE")
    app.config['DIPOE_PASSWORD'] = os.getenv("MAIL_PASS_DIPOE")
    app.config['DIPOE_SECRET'] = os.getenv("STRIPE_SECRET")
    
    app.config['GOTHIC_API'] = os.getenv("GOTHIC_API")

    
    #from .todo import todo as todo_blueprint
    #app.register_blueprint(todo_blueprint, url_prefix='/todo')
    
    from .dipoe import dipoe as dipoe_blueprint
    app.register_blueprint(dipoe_blueprint, url_prefix='/dipoe')
    
    from .gothic import gothic as gothic_blueprint
    app.register_blueprint(gothic_blueprint, url_prefix='/gothic')
    
    from .graph import graph as graph_blueprint
    app.register_blueprint(graph_blueprint, url_prefix='/graph')
    
    from .portfolio import portfolio as portfolio_blueprint
    app.register_blueprint(portfolio_blueprint)
    
    #from .skapiec import skapiec as skapiec_blueprint
    #app.register_blueprint(skapiec_blueprint, url_prefix='/skapiec')
    
    from .warhammer import warhammer as warhammer_blueprint
    app.register_blueprint(warhammer_blueprint, url_prefix='/warhammer')

    return app