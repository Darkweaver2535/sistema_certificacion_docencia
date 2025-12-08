from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Registrar blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.docentes import docentes_bp
    from app.blueprints.criterios import criterios_bp
    from app.blueprints.certificados import certificados_bp
    from app.blueprints.public import public_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(docentes_bp)
    app.register_blueprint(criterios_bp)
    app.register_blueprint(certificados_bp)
    app.register_blueprint(public_bp)
    
    return app
