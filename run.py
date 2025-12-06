from app import create_app, db
from app.models.usuario import Usuario
from app.models.unidad_academica import UnidadAcademica
from app.models.docente import Docente
from app.models.tipo_criterio import TipoCriterio
from app.models.docente_criterio import DocenteCriterio
from app.models.certificado import Certificado

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
    # host='0.0.0.0' permite acceso desde otras computadoras en la red
    # port=5000 es el puerto donde correrá la aplicación
    # debug=False en producción para mayor seguridad
    app.run(debug=True, host='0.0.0.0', port=5000)
