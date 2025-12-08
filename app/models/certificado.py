from app import db
from datetime import datetime

class Certificado(db.Model):
    """Modelo para certificados generados (uno por cada criterio del docente)"""
    __tablename__ = 'certificados'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    docente_criterio_id = db.Column(db.Integer, db.ForeignKey('docentes_criterios.id'), unique=True, nullable=False)
    
    # Código único alfanumérico (formato: ABCD-1234-EFGH)
    codigo_unico = db.Column(db.String(14), unique=True, nullable=False, index=True)
    
    # Código EMI (formato: EMI-DNICYT-CERT.00001/2025)
    codigo_emi = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Hash de verificación (HMAC-SHA256 para validar autenticidad)
    hash_verificacion = db.Column(db.String(128), nullable=False)
    
    # Ruta del QR code generado
    qr_path = db.Column(db.String(255))
    
    # Fechas
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultima_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Estado
    valido = db.Column(db.Boolean, default=True)
    
    # Relación con DocenteCriterio (uno a uno - un criterio tiene máximo un certificado)
    docente_criterio = db.relationship('DocenteCriterio', backref=db.backref('certificado', uselist=False), lazy=True)
    
    def __repr__(self):
        return f'<Certificado {self.codigo_emi} - Docente:{self.docente_id}>'
