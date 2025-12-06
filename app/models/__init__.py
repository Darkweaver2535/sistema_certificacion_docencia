# Archivo de inicialización del paquete models
from app.models.usuario import Usuario
from app.models.unidad_academica import UnidadAcademica
from app.models.docente import Docente
from app.models.tipo_criterio import TipoCriterio
from app.models.docente_criterio import DocenteCriterio
from app.models.certificado import Certificado

__all__ = [
    'Usuario',
    'UnidadAcademica',
    'Docente',
    'TipoCriterio',
    'DocenteCriterio',
    'Certificado'
]
