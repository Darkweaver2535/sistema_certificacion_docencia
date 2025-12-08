from app import db
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import relationship

class Docente(db.Model):
    """Modelo simplificado para docentes de la EMI"""
    __tablename__ = 'docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    
    # Control de regeneración de certificado
    requiere_regeneracion = db.Column(db.Boolean, default=True)
    
    # Metadata
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    criterios = db.relationship('DocenteCriterio', backref='docente', lazy='dynamic', 
                               cascade='all, delete-orphan',
                               order_by='DocenteCriterio.tipo_criterio_id')
    certificados = db.relationship('Certificado', backref='docente', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Docente {self.nombre_completo}>'
