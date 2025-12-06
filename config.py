import os
from dotenv import load_dotenv

load_dotenv()

# Directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Obtener DATABASE_URL y convertir postgres:// a postgresql:// si es necesario
    # Render y Heroku usan postgres:// pero SQLAlchemy 1.4+ requiere postgresql://
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///emi_certificacion.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'importaciones')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Configuración de QR codes
    QR_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'qr_codes')
    
    # Configuración de certificados
    CERTIFICATE_TEMPLATE = os.path.join(BASE_DIR, 'MODELO_1_CERTIFICACION DE PRODUCCIÓN INTELECTUAL Y CIENTÍFICA.docx')
    
    # Salt para generación de códigos únicos (cambiar en producción)
    CERTIFICATE_SALT = os.environ.get('CERTIFICATE_SALT') or 'emi-cert-salt-2025'
    
    # URL base para códigos QR (opcional, se detecta automáticamente de la solicitud)
    # Útil si usas un dominio específico o proxy reverso
    BASE_URL = os.environ.get('BASE_URL') or None
