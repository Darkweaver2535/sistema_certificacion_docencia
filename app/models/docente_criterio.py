from app import db
from datetime import datetime

class DocenteCriterio(db.Model):
    """Modelo para la relación entre docentes y criterios (con detalles)"""
    __tablename__ = 'docentes_criterios'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    tipo_criterio_id = db.Column(db.Integer, db.ForeignKey('tipos_criterios.id'), nullable=False)
    
    # Detalles del criterio (texto libre, se mostrará en el certificado)
    detalles = db.Column(db.Text, nullable=False)
    
    # Metadata
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('docente_id', 'tipo_criterio_id', name='uq_docente_criterio'),
    )
    
    def __repr__(self):
        return f'<DocenteCriterio Docente:{self.docente_id} Criterio:{self.tipo_criterio_id}>'
