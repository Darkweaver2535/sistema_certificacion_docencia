#!/usr/bin/env python3
"""
Script de migración: Combinar nombres y apellidos en nombre_completo
"""
from app import create_app, db
from app.models.docente import Docente
from sqlalchemy import text

def migrate():
    app = create_app()
    
    with app.app_context():
        print("Iniciando migración de estructura de docentes...")
        print("=" * 50)
        
        # Verificar si ya existe la columna nombre_completo
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('docentes')]
        
        if 'nombre_completo' in columns and 'nombres' in columns:
            print("\n✅ Detectada estructura antigua (nombres + apellidos)")
            print("   Migrando a estructura nueva (nombre_completo)...")
            
            # Obtener todos los docentes
            docentes = db.session.execute(
                text("SELECT id, nombres, apellidos FROM docentes WHERE activo = true")
            ).fetchall()
            
            print(f"\n📊 Encontrados {len(docentes)} docentes activos")
            
            # Actualizar cada docente
            for docente in docentes:
                nombre_completo = f"{docente.nombres} {docente.apellidos}".strip()
                db.session.execute(
                    text("UPDATE docentes SET nombre_completo = :nombre WHERE id = :id"),
                    {"nombre": nombre_completo, "id": docente.id}
                )
                print(f"   ✓ {docente.id}: {nombre_completo}")
            
            db.session.commit()
            print(f"\n✅ Migración completada: {len(docentes)} docentes actualizados")
            
            # Ahora eliminar las columnas antiguas (SQLite requiere recrear la tabla)
            print("\n⚠️  ADVERTENCIA: Para eliminar las columnas 'nombres' y 'apellidos'")
            print("   necesitas ejecutar las siguientes acciones manualmente:")
            print("\n   Si usas SQLite:")
            print("   1. Hacer backup de la base de datos")
            print("   2. Las columnas antiguas quedarán en la BD pero no se usarán")
            print("\n   Si usas PostgreSQL:")
            print("   ALTER TABLE docentes DROP COLUMN nombres;")
            print("   ALTER TABLE docentes DROP COLUMN apellidos;")
            
        elif 'nombre_completo' in columns and 'nombres' not in columns:
            print("\n✅ Base de datos ya está en la nueva estructura")
            print("   No se requiere migración")
            
        else:
            print("\n❌ Estructura desconocida de base de datos")
            print(f"   Columnas encontradas: {columns}")
            return False
        
        print("\n" + "=" * 50)
        print("Migración finalizada")
        return True

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════╗
║   MIGRACIÓN: nombres/apellidos → nombre_completo       ║
║   Sistema de Certificación EMI                         ║
╚════════════════════════════════════════════════════════╝
    """)
    
    respuesta = input("¿Desea continuar con la migración? (SI/no): ")
    
    if respuesta.upper() == "SI":
        success = migrate()
        if success:
            print("\n✅ Proceso completado exitosamente")
        else:
            print("\n❌ Hubo errores en la migración")
    else:
        print("\n❌ Migración cancelada")
