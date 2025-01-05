
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from config import Config
import os
import pymysql

load_dotenv()
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app