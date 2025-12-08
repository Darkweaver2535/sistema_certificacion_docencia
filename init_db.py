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
            TipoCriterio(nombre='TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE - EMI', descripcion='Ponencias en talleres, congresos, simposios o seminarios dentro de EMI', orden=1),
            TipoCriterio(nombre='TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE', descripcion='Ponencias en talleres, congresos, simposios o seminarios fuera de EMI', orden=2),
            TipoCriterio(nombre='TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS-EMI', descripcion='Textos académicos, guías, manuales o videos educativos en EMI', orden=3),
            TipoCriterio(nombre='TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS', descripcion='Textos académicos, guías, manuales o videos educativos fuera de EMI', orden=4),
            TipoCriterio(nombre='LIBROS (SENAPI o ISBN) - EMI', descripcion='Libros con registro SENAPI o ISBN publicados en EMI', orden=5),
            TipoCriterio(nombre='LIBROS (SENAPI o ISBN)', descripcion='Libros con registro SENAPI o ISBN publicados fuera de EMI', orden=6),
            TipoCriterio(nombre='ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA) - EMI', descripcion='Artículos académicos de opinión, reflexión o revisión bibliográfica en EMI', orden=7),
            TipoCriterio(nombre='ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA)', descripcion='Artículos académicos de opinión, reflexión o revisión bibliográfica fuera de EMI', orden=8),
            TipoCriterio(nombre='ARTÍCULOS CIENTÍFICOS INDEXADOS (QS) - EMI', descripcion='Artículos científicos publicados en revistas indexadas QS en EMI', orden=9),
            TipoCriterio(nombre='ARTÍCULOS CIENTÍFICOS INDEXADOS (QS)', descripcion='Artículos científicos publicados en revistas indexadas QS fuera de EMI', orden=10),
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
