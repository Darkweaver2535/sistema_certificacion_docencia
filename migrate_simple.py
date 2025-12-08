"""
Script de migración para versión simplificada
Elimina restricciones NOT NULL de campos removidos en el modelo Docente
"""
import os
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Migrando base de datos a versión simplificada...")
    
    # Hacer nullable todos los campos que ya no se usan
    campos_a_nullable = ['ci', 'unidad_academica_id', 'cargo', 'años_servicio', 'email', 'telefono', 'foto']
    
    for campo in campos_a_nullable:
        try:
            sql = f"ALTER TABLE docentes ALTER COLUMN {campo} DROP NOT NULL;"
            db.session.execute(text(sql))
            print(f"✅ Campo '{campo}' ahora es nullable")
        except Exception as e:
            print(f"⚠️  Campo '{campo}': {str(e)}")
    
    try:
        db.session.commit()
        print("\n✅ Migración completada exitosamente")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error al aplicar migración: {e}")
