from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SESSION_TYPE'] = 'filesystem'
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    Session(app)
    CORS(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Create database tables automatically in development mode
    @app.before_request
    def create_tables():
        if app.config.get("FLASK_ENV") == "development":  # Only in development
            db.create_all()

    return app
