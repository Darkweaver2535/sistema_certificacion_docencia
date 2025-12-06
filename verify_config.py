#!/usr/bin/env python
"""
Script de verificación de configuración para Render
Ejecuta este script en el Shell de Render para verificar que todo esté configurado correctamente
"""

import os
import sys

def check_environment():
    """Verifica las variables de entorno necesarias"""
    print("=" * 60)
    print("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    print("=" * 60)
    
    required_vars = {
        'DATABASE_URL': 'URL de conexión a PostgreSQL',
        'SECRET_KEY': 'Clave secreta de Flask',
        'CERTIFICATE_SALT': 'Salt para códigos únicos'
    }
    
    optional_vars = {
        'FLASK_APP': 'Archivo principal de Flask',
        'FLASK_ENV': 'Ambiente de Flask',
        'BASE_URL': 'URL base para códigos QR',
        'PORT': 'Puerto del servidor'
    }
    
    print("\n✅ Variables REQUERIDAS:")
    all_required_ok = True
    for var, desc in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Ocultar valores sensibles
            if var in ['SECRET_KEY', 'CERTIFICATE_SALT', 'DATABASE_URL']:
                display_value = value[:10] + '...' if len(value) > 10 else '***'
            else:
                display_value = value
            print(f"  ✓ {var}: {display_value} ({desc})")
        else:
            print(f"  ✗ {var}: NO CONFIGURADA ({desc})")
            all_required_ok = False
    
    print("\n📋 Variables OPCIONALES:")
    for var, desc in optional_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"  ✓ {var}: {value} ({desc})")
        else:
            print(f"  - {var}: No configurada ({desc})")
    
    return all_required_ok

def check_database_url():
    """Verifica el formato de DATABASE_URL"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE DATABASE_URL")
    print("=" * 60)
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL no está configurada")
        return False
    
    print(f"\n🔍 URL original: {database_url[:30]}...")
    
    # Verificar el esquema
    if database_url.startswith('postgres://'):
        print("⚠️  La URL usa postgres:// (será convertida a postgresql://)")
        converted_url = database_url.replace('postgres://', 'postgresql://', 1)
        print(f"✅ URL convertida: {converted_url[:30]}...")
    elif database_url.startswith('postgresql://'):
        print("✅ La URL usa postgresql:// (correcto para SQLAlchemy 1.4+)")
    else:
        print(f"❌ Esquema desconocido: {database_url.split('://')[0]}")
        return False
    
    return True

def check_database_connection():
    """Intenta conectarse a la base de datos"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE CONEXIÓN A BASE DE DATOS")
    print("=" * 60)
    
    try:
        from config import Config
        from sqlalchemy import create_engine
        
        print(f"\n🔗 Intentando conectar a: {Config.SQLALCHEMY_DATABASE_URI[:30]}...")
        
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        
        # Ejecutar consulta simple
        result = connection.execute("SELECT version();")
        version = result.fetchone()[0]
        
        print(f"✅ Conexión exitosa!")
        print(f"📊 PostgreSQL version: {version}")
        
        connection.close()
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print("   Asegúrate de haber ejecutado: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n💡 Posibles causas:")
        print("   1. DATABASE_URL no está configurada correctamente en Render")
        print("   2. La base de datos PostgreSQL no está creada")
        print("   3. La base de datos está en una región diferente al Web Service")
        print("   4. Problemas de red o firewall")
        return False

def check_folders():
    """Verifica que existan las carpetas necesarias"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE CARPETAS")
    print("=" * 60)
    
    from config import Config
    
    folders = {
        'QR_FOLDER': Config.QR_FOLDER,
        'UPLOAD_FOLDER': Config.UPLOAD_FOLDER,
    }
    
    print()
    for name, path in folders.items():
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"⚠️  {name}: {path} (no existe, se creará automáticamente)")
    
    return True

def check_template():
    """Verifica que exista el template de certificado"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE TEMPLATE DE CERTIFICADO")
    print("=" * 60)
    
    from config import Config
    
    template_path = Config.CERTIFICATE_TEMPLATE
    print(f"\n📄 Ruta del template: {template_path}")
    
    if os.path.exists(template_path):
        size = os.path.getsize(template_path)
        print(f"✅ Template encontrado ({size:,} bytes)")
        return True
    else:
        print("❌ Template NO encontrado")
        print("\n💡 Acción requerida:")
        print(f"   Debes subir el archivo de template a: {template_path}")
        print("   O ajustar la ruta en config.py")
        return False

def main():
    """Ejecuta todas las verificaciones"""
    print("\n🔍 VERIFICACIÓN DE CONFIGURACIÓN - Sistema de Certificación EMI")
    print("=" * 60)
    
    results = {
        'Variables de entorno': check_environment(),
        'Formato DATABASE_URL': check_database_url(),
        'Conexión a base de datos': check_database_connection(),
        'Carpetas del sistema': check_folders(),
        'Template de certificado': check_template(),
    }
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    for check, result in results.items():
        status = "✅ OK" if result else "❌ FALLO"
        print(f"{status} - {check}")
    
    all_ok = all(results.values())
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 ¡Todas las verificaciones pasaron exitosamente!")
        print("   El sistema está listo para usarse.")
    else:
        print("⚠️  Algunas verificaciones fallaron.")
        print("   Revisa los mensajes arriba y corrige los problemas.")
        print("   Consulta DEPLOYMENT_RENDER.md para más detalles.")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
