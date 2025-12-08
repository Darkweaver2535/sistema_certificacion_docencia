from app import db
from datetime import datetime

class UnidadAcademica(db.Model):
    """Modelo para las unidades académicas de la EMI"""
    __tablename__ = 'unidades_academicas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False, index=True)  # UALP, UACB, etc.
    nombre = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    docentes = db.relationship('Docente', backref='unidad', lazy='dynamic')
    
    def __repr__(self):
        return f'<UnidadAcademica {self.codigo} - {self.ciudad}>'
