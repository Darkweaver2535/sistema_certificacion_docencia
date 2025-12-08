#!/usr/bin/env python
"""
Script de inicialización de base de datos
Se ejecuta automáticamente si la base de datos no existe
"""

from app import create_app, db
from app.models.usuario import Usuario
from app.models.tipo_criterio import TipoCriterio

def init_database():
    """Inicializa la base de datos con datos por defecto"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creando tablas de base de datos...")
        db.create_all()
        
        # Verificar si ya hay datos
        if Usuario.query.first() is not None:
            print("✅ La base de datos ya está inicializada")
            return
        
        print("📝 Creando usuario administrador...")
        admin = Usuario(username='admin', nombre_completo='Administrador EMI')
        admin.set_password('admin123')
        db.session.add(admin)
        
        print("📋 Creando criterios de certificación...")
        criterios = [
            TipoCriterio(nombre='Libros publicados', descripcion='Autoría o coautoría de libros académicos', orden=1),
            TipoCriterio(nombre='Artículos en revistas indexadas', descripcion='Publicaciones en revistas científicas indexadas', orden=2),
            TipoCriterio(nombre='Capítulos de libros', descripcion='Contribuciones en libros académicos', orden=3),
            TipoCriterio(nombre='Ponencias en congresos', descripcion='Presentaciones en eventos académicos', orden=4),
            TipoCriterio(nombre='Proyectos de investigación', descripcion='Dirección o participación en proyectos de investigación', orden=5),
            TipoCriterio(nombre='Tesis dirigidas', descripcion='Dirección de tesis de grado o posgrado', orden=6),
            TipoCriterio(nombre='Patentes o registros', descripcion='Patentes de invención o registros de propiedad intelectual', orden=7),
            TipoCriterio(nombre='Premios y reconocimientos', descripcion='Premios académicos o científicos recibidos', orden=8),
            TipoCriterio(nombre='Formación académica avanzada', descripcion='Maestrías, Doctorados, Posdoctorados', orden=9),
            TipoCriterio(nombre='Participación en redes académicas', descripcion='Membresía en sociedades científicas o redes de investigación', orden=10),
        ]
        db.session.add_all(criterios)
        
        print("💾 Guardando cambios en la base de datos...")
        db.session.commit()
        
        print("✅ Base de datos inicializada correctamente")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer login")

if __name__ == '__main__':
    init_database()
