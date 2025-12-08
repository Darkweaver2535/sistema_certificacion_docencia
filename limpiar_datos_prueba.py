#!/usr/bin/env python
"""
Script para limpiar todos los datos de prueba de la base de datos
ADVERTENCIA: Este script eliminará TODOS los docentes, certificados y criterios
"""

from app import create_app, db
from app.models.docente import Docente
from app.models.certificado import Certificado
from app.models.docente_criterio import DocenteCriterio
import os
import shutil

def limpiar_datos():
    app = create_app()
    
    with app.app_context():
        print("🗑️  Limpiando datos de prueba...")
        print("-" * 50)
        
        # Contar registros antes de eliminar
        total_certificados = Certificado.query.count()
        total_criterios = DocenteCriterio.query.count()
        total_docentes = Docente.query.count()
        
        print(f"📊 Registros encontrados:")
        print(f"   - Certificados: {total_certificados}")
        print(f"   - Criterios de docentes: {total_criterios}")
        print(f"   - Docentes: {total_docentes}")
        print()
        
        if total_docentes == 0:
            print("✅ No hay datos para eliminar.")
            return
        
        # Confirmación
        respuesta = input("⚠️  ¿Está seguro de eliminar TODOS los datos? (escriba 'SI' para confirmar): ")
        
        if respuesta.strip().upper() != 'SI':
            print("❌ Operación cancelada.")
            return
        
        try:
            # 1. Eliminar certificados
            print("\n🔄 Eliminando certificados...")
            Certificado.query.delete()
            db.session.commit()
            print(f"   ✅ {total_certificados} certificados eliminados")
            
            # 2. Eliminar códigos QR
            print("\n🔄 Eliminando códigos QR...")
            qr_folder = 'app/static/qr_codes'
            if os.path.exists(qr_folder):
                archivos_qr = [f for f in os.listdir(qr_folder) if f.endswith('.png')]
                for archivo in archivos_qr:
                    os.remove(os.path.join(qr_folder, archivo))
                print(f"   ✅ {len(archivos_qr)} archivos QR eliminados")
            
            # 3. Eliminar criterios de docentes
            print("\n🔄 Eliminando criterios de docentes...")
            DocenteCriterio.query.delete()
            db.session.commit()
            print(f"   ✅ {total_criterios} criterios eliminados")
            
            # 4. Eliminar docentes
            print("\n🔄 Eliminando docentes...")
            Docente.query.delete()
            db.session.commit()
            print(f"   ✅ {total_docentes} docentes eliminados")
            
            print("\n" + "=" * 50)
            print("✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
            print("=" * 50)
            print("\n💡 La base de datos está lista para producción.")
            print("   Usuarios del sistema NO fueron eliminados.\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error durante la limpieza: {str(e)}")
            print("   Los cambios fueron revertidos.")

if __name__ == '__main__':
    limpiar_datos()
