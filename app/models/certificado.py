from app import db
from datetime import datetime

class Certificado(db.Model):
    """Modelo para certificados generados (uno por docente)"""
    __tablename__ = 'certificados'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), unique=True, nullable=False)
    
    # Código único alfanumérico (formato: ABCD-1234-EFGH)
    codigo_unico = db.Column(db.String(14), unique=True, nullable=False, index=True)
    
    # Hash de verificación (HMAC-SHA256 para validar autenticidad)
    hash_verificacion = db.Column(db.String(128), nullable=False)
    
    # Ruta del QR code generado
    qr_path = db.Column(db.String(255))
    
    # Fechas
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Estado
    valido = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Certificado {self.codigo_unico} - Docente:{self.docente_id}>'
