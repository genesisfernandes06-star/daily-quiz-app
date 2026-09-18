from flask import Flask
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)
    CORS(app) 
    
    # ⚠️ IMPORTANT: Change 'your_pgadmin_password' to your actual PostgreSQL password
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1111@localhost/quiz_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from . import routes
    app.register_blueprint(routes.main)
    
    return app