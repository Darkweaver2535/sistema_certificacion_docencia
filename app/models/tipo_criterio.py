from app import db
from datetime import datetime

class TipoCriterio(db.Model):
    """Modelo para los tipos de criterios de producción intelectual y científica"""
    __tablename__ = 'tipos_criterios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    orden = db.Column(db.Integer)  # Para mantener el orden de visualización
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    docente_criterios = db.relationship('DocenteCriterio', backref='tipo_criterio', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoCriterio {self.nombre}>'
