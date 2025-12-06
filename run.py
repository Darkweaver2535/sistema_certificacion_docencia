from app import create_app, db
from app.models.usuario import Usuario
from app.models.unidad_academica import UnidadAcademica
from app.models.docente import Docente
from app.models.tipo_criterio import TipoCriterio
from app.models.docente_criterio import DocenteCriterio
from app.models.certificado import Certificado
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Contexto para el shell de Flask"""
    return {
        'db': db,
        'Usuario': Usuario,
        'UnidadAcademica': UnidadAcademica,
        'Docente': Docente,
        'TipoCriterio': TipoCriterio,
        'DocenteCriterio': DocenteCriterio,
        'Certificado': Certificado
    }

if __name__ == '__main__':
    # Obtener el puerto de la variable de entorno (Render lo proporciona)
    # Si no existe, usar 5000 para desarrollo local
    port = int(os.environ.get('PORT', 5000))
    
    # host='0.0.0.0' permite acceso desde otras computadoras en la red
    # debug=False en producción para mayor seguridad
    app.run(debug=False, host='0.0.0.0', port=port)
