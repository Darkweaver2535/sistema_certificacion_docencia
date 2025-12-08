from app import create_app, db
from app.models.usuario import Usuario
from app.models.docente import Docente
from app.models.tipo_criterio import TipoCriterio
from app.models.docente_criterio import DocenteCriterio
from app.models.certificado import Certificado
import os

app = create_app()

# Inicializar base de datos si no existe
def init_db_if_needed():
    """Inicializa la base de datos automáticamente si no existe"""
    with app.app_context():
        # Verificar si las tablas existen
        inspector = db.inspect(db.engine)
        if not inspector.has_table('usuario'):
            print("🔧 Inicializando base de datos...")
            from init_db import init_database
            init_database()
        else:
            print("✅ Base de datos ya inicializada")

# Ejecutar inicialización al importar
init_db_if_needed()

@app.shell_context_processor
def make_shell_context():
    """Contexto para el shell de Flask"""
    return {
        'db': db,
        'Usuario': Usuario,
        'Docente': Docente,
        'TipoCriterio': TipoCriterio,
        'DocenteCriterio': DocenteCriterio,
        'Certificado': Certificado
    }

if __name__ == '__main__':
    # Obtener el puerto de la variable de entorno (Render lo proporciona)
    # Si no existe, usar 5001 para desarrollo local (5000 está ocupado por AirPlay en macOS)
    port = int(os.environ.get('PORT', 5001))
    
    # host='0.0.0.0' permite acceso desde otras computadoras en la red
    # debug=False en producción para mayor seguridad
    app.run(debug=False, host='0.0.0.0', port=port)
