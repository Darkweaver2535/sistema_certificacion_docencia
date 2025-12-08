"""
Migración para cambiar certificados de one-to-one a one-to-many
y agregar campos codigo_emi y docente_criterio_id
"""
import os
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔧 Migrando tabla certificados...")
    
    try:
        # 1. Eliminar restricción unique de docente_id
        print("1. Eliminando restricción unique de docente_id...")
        db.session.execute(text("""
            ALTER TABLE certificados DROP CONSTRAINT IF EXISTS certificados_docente_id_key;
        """))
        
        # 2. Agregar campo docente_criterio_id
        print("2. Agregando campo docente_criterio_id...")
        db.session.execute(text("""
            ALTER TABLE certificados 
            ADD COLUMN IF NOT EXISTS docente_criterio_id INTEGER;
        """))
        
        # 3. Agregar campo codigo_emi
        print("3. Agregando campo codigo_emi...")
        db.session.execute(text("""
            ALTER TABLE certificados 
            ADD COLUMN IF NOT EXISTS codigo_emi VARCHAR(50);
        """))
        
        # 4. Agregar foreign key para docente_criterio_id
        print("4. Agregando foreign key para docente_criterio_id...")
        db.session.execute(text("""
            ALTER TABLE certificados 
            ADD CONSTRAINT fk_certificados_docente_criterio 
            FOREIGN KEY (docente_criterio_id) 
            REFERENCES docentes_criterios(id) 
            ON DELETE CASCADE;
        """))
        
        # 5. Agregar unique constraint a docente_criterio_id
        print("5. Agregando unique constraint a docente_criterio_id...")
        db.session.execute(text("""
            ALTER TABLE certificados 
            ADD CONSTRAINT uq_certificados_docente_criterio 
            UNIQUE (docente_criterio_id);
        """))
        
        # 6. Agregar unique constraint a codigo_emi
        print("6. Agregando unique constraint a codigo_emi...")
        db.session.execute(text("""
            ALTER TABLE certificados 
            ADD CONSTRAINT uq_certificados_codigo_emi 
            UNIQUE (codigo_emi);
        """))
        
        # 7. Eliminar certificados existentes (ya que la estructura cambió completamente)
        print("7. Limpiando certificados antiguos...")
        db.session.execute(text("DELETE FROM certificados;"))
        
        db.session.commit()
        print("\n✅ Migración completada exitosamente")
        print("ℹ️  Los certificados antiguos fueron eliminados. Genere nuevamente los certificados por criterio.")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        print("\nSi el error persiste, puede ser necesario recrear la tabla certificados manualmente.")
