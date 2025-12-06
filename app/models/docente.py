from app import db
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import relationship

class Docente(db.Model):
    """Modelo para docentes de la EMI"""
    __tablename__ = 'docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Información laboral
    unidad_academica_id = db.Column(db.Integer, db.ForeignKey('unidades_academicas.id'), nullable=False)
    cargo = db.Column(db.String(150))
    años_servicio = db.Column(db.Integer)
    
    # Información de contacto
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    foto = db.Column(db.String(255))  # Opcional
    
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
    certificado = db.relationship('Certificado', backref='docente', uselist=False, cascade='all, delete-orphan')
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del docente"""
        return f"{self.nombres} {self.apellidos}"
    
    def __repr__(self):
        return f'<Docente {self.nombre_completo} - CI: {self.ci}>'
