from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='views/templates', 
                static_folder='views/static')       
    app.config.from_object(Config)
    
    db.init_app(app)
    
    from app.controllers.recipe_controller import recipe_bp
    app.register_blueprint(recipe_bp)
    
    return app