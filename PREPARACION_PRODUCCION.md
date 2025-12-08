# RESUMEN DE PREPARACIÓN PARA PRODUCCIÓN
## Sistema de Certificación Docente EMI

### ✅ ARCHIVOS CREADOS PARA PRODUCCIÓN

#### 1. Scripts de Utilidad
- **limpiar_datos_prueba.py**: Elimina todos los datos de prueba
  - Borra: Certificados, DocenteCriterio, Docentes
  - Elimina: Archivos QR PNG
  - Conserva: Usuarios y TipoCriterio
  - Requiere confirmación "SI"

#### 2. Configuración para Windows
- **sistema_certificacion.spec**: Configuración de PyInstaller
  - Genera: SistemaCertificacionEMI.exe
  - Incluye: templates, static, .env, config.py
  - Modo: Consola (para ver logs)

- **iniciar.bat**: Script de inicio rápido
  - Crea .env automático si no existe
  - Inicia el ejecutable
  - Abre navegador en http://localhost:5001
  - Muestra credenciales por defecto

#### 3. Documentación
- **INSTALACION_WINDOWS.md**: Manual completo
  - Instalación de PostgreSQL
  - Configuración de base de datos
  - Configuración de .env
  - Primer uso
  - Solución de problemas
  - Respaldo y restauración

- **INSTRUCCIONES_COMPILACION.md**: Guía de compilación
  - Opción 1: GitHub Actions (automático)
  - Opción 2: Compilación manual en Windows
  - Creación del paquete de distribución
  - Pruebas del ejecutable

#### 4. Automatización CI/CD
- **.github/workflows/build-windows.yml**: GitHub Actions
  - Se ejecuta en cada push a rama "simple"
  - Genera ejecutable automáticamente
  - Crea paquete ZIP listo para distribuir
  - Sube artifact a GitHub (90 días)

### 📋 PASOS PENDIENTES

#### A. Limpiar Datos de Prueba

```bash
# 1. Detener el servidor Flask (Ctrl+C)
# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Ejecutar limpieza
python limpiar_datos_prueba.py

# 4. Confirmar con: SI
```

#### B. Generar Ejecutable (REQUIERE WINDOWS)

**Opción Automática (Recomendada):**
```bash
# 1. Commit de todos los archivos nuevos
git add .
git commit -m "Preparación para producción Windows"
git push origin simple

# 2. Ir a GitHub → Actions → Esperar compilación
# 3. Descargar artifact "SistemaCertificacionEMI-Windows"
```

**Opción Manual (en Windows):**
```cmd
# 1. Clonar repositorio
git clone https://github.com/Darkweaver2535/sistema_certificacion_docencia.git
cd sistema_certificacion_docencia
git checkout simple

# 2. Crear entorno
python -m venv venv
venv\Scripts\activate

# 3. Instalar
pip install -r requirements.txt
pip install pyinstaller

# 4. Compilar
pyinstaller sistema_certificacion.spec

# 5. El ejecutable estará en: dist\SistemaCertificacionEMI.exe
```

### 📦 CONTENIDO DEL PAQUETE FINAL

El archivo `SistemaCertificacionEMI.zip` incluirá:
```
SistemaCertificacionEMI.zip
├── SistemaCertificacionEMI.exe    (Aplicación principal)
├── .env                            (Configuración de BD)
├── iniciar.bat                     (Iniciador rápido)
├── INSTALACION_WINDOWS.md          (Manual completo)
└── LEEME.txt                       (Instrucciones básicas)
```

### 🔧 CONFIGURACIÓN ACTUAL DEL SISTEMA

#### Base de Datos
- Motor: PostgreSQL
- Host: localhost:5432
- Database: certificacion_emi
- Usuario: postgres
- Respaldo: Automático desde dashboard

#### Códigos de Certificado
- **Alfanumérico**: ABCD-1234-EFGH (formato visual)
- **EMI**: EMI-DNICYT-CERT.00001/2025 (formato oficial)
- Generación: HMAC-SHA256 basado en timestamp

#### Códigos QR
- Tamaño: 400px (visual óptimo)
- Contenido: Nombre, códigos, criterio, descripción (200 chars)
- Formato: PNG
- Ubicación: app/static/qr_codes/
- Corrección de errores: Media

#### Flujo de Trabajo
1. Crear Docente → Auto-redirige a Gestionar Criterios
2. Agregar Criterios → Guardar
3. Generar Certificados → Permanece en vista del docente
4. Descargar QR individual

#### Usuario Administrador
- Usuario: admin
- Contraseña: admin123
- **IMPORTANTE**: Cambiar en primera ejecución

### ⚠️ NOTAS IMPORTANTES

1. **PostgreSQL es REQUISITO**: El usuario final debe instalarlo
2. **Antivirus**: Puede marcar el .exe como falso positivo
3. **Tamaño**: Ejecutable ~50-80 MB
4. **Python NO requerido**: El ejecutable es independiente
5. **Puerto 5001**: Debe estar libre en el sistema del usuario

### 🎯 PRÓXIMOS PASOS RECOMENDADOS

1. **Ejecutar limpieza de datos** (cuando esté listo para producción)
2. **Hacer commit y push** para activar GitHub Actions
3. **Descargar ejecutable** generado por Actions
4. **Probar en Windows limpio** (sin Python instalado)
5. **Distribuir ZIP** a usuarios finales

### 📞 SOPORTE

Para usuarios finales:
- Leer primero: INSTALACION_WINDOWS.md
- Problemas comunes: Sección "Solución de Problemas"
- Credenciales olvidadas: Ver archivo .env

---
**Fecha de preparación**: 2025-01-13
**Versión**: 1.0
**Rama**: simple
**Estado**: Listo para compilación en Windows
