# Sistema de Certificación Docente EMI

Sistema web desarrollado en Flask para la gestión y certificación de la producción intelectual y científica del plantel docente de la Escuela Militar de Ingeniería (EMI) de Bolivia.

## 🎯 Características Principales

- ✅ **Gestión de Docentes**: CRUD completo con registro manual y carga masiva desde Excel/CSV
- ✅ **Unidades Académicas**: Soporte para las 5 unidades (UALP, UACB, UASC, UARB, UATP)
- ✅ **10 Criterios de Producción**: Gestión de talleres, textos, libros, artículos científicos, etc.
- ✅ **Generación de Certificados PDF**: Basados en plantilla Word con código único y QR
- ✅ **Verificación Pública**: Sistema de verificación mediante código QR sin autenticación
- ✅ **Códigos Únicos Criptográficos**: Formato ABCD-1234-EFGH con HMAC-SHA256
- ✅ **Dashboard Administrativo**: Estadísticas y gestión centralizada

## 📋 Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- LibreOffice (para conversión Word a PDF en macOS/Linux) o Microsoft Word (Windows)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
cd ~/Desktop/sistema_de_certificacion_docentes
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Crear la base de datos:

```bash
psql -U postgres
CREATE DATABASE emi_certificacion;
\q
```

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/emi_certificacion
FLASK_APP=run.py
FLASK_ENV=development
CERTIFICATE_SALT=emi-salt-produccion-2025
```

### 6. Inicializar la base de datos

```bash
# Crear todas las tablas
flask init-db

# Poblar datos iniciales (5 unidades académicas y 10 criterios)
flask seed-data

# Crear usuario administrador
flask create-admin
```

Cuando ejecutes `flask create-admin`, se te pedirá:
- Nombre de usuario
- Contraseña
- Nombre completo
- Email

### 7. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📚 Uso del Sistema

### Login Administrativo

1. Acceder a `http://localhost:5000/auth/login`
2. Ingresar credenciales del administrador
3. Acceder al dashboard

### Registrar Docentes

**Opción 1: Registro Individual**
1. Dashboard → Nuevo Docente
2. Completar formulario con datos del docente
3. Guardar

**Opción 2: Importación Masiva**
1. Dashboard → Importar desde Excel
2. Descargar plantilla Excel
3. Completar plantilla con datos (columnas requeridas):
   - `nombres`
   - `apellidos`
   - `ci`
   - `unidad_codigo` (UALP, UACB, UASC, UARB, UATP)
   - `cargo`
   - `años_servicio`
   - `email` (opcional)
   - `telefono` (opcional)
4. Subir archivo
5. Revisar reporte de importación

### Gestionar Criterios de un Docente

1. Listado de Docentes → Ver docente
2. Gestionar Criterios
3. Marcar criterios aplicables
4. Ingresar detalles en el campo de texto
5. Guardar

Los 10 criterios disponibles son:
1. TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE - EMI
2. TALLERES Y CONGRESOS, SIMPOSIOS O SEMINARIOS COMO PONENTE
3. TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS - EMI
4. TEXTOS ACADÉMICOS, GUÍAS, MANUALES, VIDEOS EDUCATIVOS
5. LIBROS (SENAPI o ISBN) - EMI
6. LIBROS (SENAPI o ISBN)
7. ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA) - EMI
8. ARTÍCULOS ACADÉMICOS (OPINIÓN, REFLEXIÓN, REV. BIBLIOGRÁFICA)
9. ARTÍCULOS CIENTÍFICOS INDEXADOS (QS) - EMI
10. ARTÍCULOS CIENTÍFICOS INDEXADOS (QS)

### Generar Certificados

1. Ver docente con criterios registrados
2. Generar Certificado
3. El sistema:
   - Genera código único (ej: ABCD-1234-EFGH)
   - Crea código QR para verificación
   - Procesa plantilla Word con datos del docente
   - Convierte a PDF
   - Descarga automáticamente

### Verificación Pública

1. Escanear código QR del certificado
2. O ingresar manualmente a `http://localhost:5000/verificar/<codigo>`
3. Ver información del docente y criterios
4. Validar autenticidad

## 🗂️ Estructura del Proyecto

```
sistema_de_certificacion_docentes/
├── app/
│   ├── __init__.py              # Factory de aplicación Flask
│   ├── blueprints/              # Módulos de rutas
│   │   ├── auth.py              # Autenticación y dashboard
│   │   ├── docentes.py          # CRUD de docentes
│   │   ├── criterios.py         # Gestión de criterios
│   │   ├── certificados.py      # Generación de certificados
│   │   └── public.py            # Verificación pública
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── usuario.py
│   │   ├── unidad_academica.py
│   │   ├── docente.py
│   │   ├── tipo_criterio.py
│   │   ├── docente_criterio.py
│   │   └── certificado.py
│   ├── templates/               # Plantillas HTML
│   ├── static/                  # Archivos estáticos (CSS, JS)
│   │   └── qr_codes/            # Códigos QR generados
│   ├── utils/                   # Utilidades
│   │   └── __init__.py          # CertificadoGenerator
│   └── commands.py              # Comandos CLI Flask
├── uploads/
│   └── importaciones/           # Archivos Excel/CSV importados
├── config.py                    # Configuración de la aplicación
├── run.py                       # Punto de entrada
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno (no en git)
├── .env.example                 # Ejemplo de variables de entorno
├── .gitignore                   # Archivos ignorados por git
└── README.md                    # Este archivo
```

## 🔧 Comandos Flask CLI

```bash
# Inicializar base de datos
flask init-db

# Poblar datos iniciales
flask seed-data

# Crear usuario administrador
flask create-admin

# Abrir shell interactivo
flask shell
```

## 📝 Plantilla de Certificado

El sistema utiliza el archivo Word `MODELO_1_CERTIFICACION DE PRODUCCIÓN INTELECTUAL Y CIENTÍFICA.docx` como plantilla.

**Placeholders soportados:**
- `{{NOMBRE}}` - Nombre completo del docente
- `{{NOMBRES}}` - Solo nombres
- `{{APELLIDOS}}` - Solo apellidos
- `{{CI}}` - Cédula de identidad
- `{{UNIDAD}}` - Nombre completo de unidad académica
- `{{UNIDAD_CODIGO}}` - Código de unidad (UALP, etc.)
- `{{CIUDAD}}` - Ciudad de la unidad
- `{{CARGO}}` - Cargo del docente
- `{{AÑOS_SERVICIO}}` - Años de servicio
- `{{FECHA}}` - Fecha de generación
- `{{QR}}` - Código QR (se inserta como imagen)

## 🔐 Seguridad

- **Códigos Únicos**: Generados con HMAC-SHA256 + salt secreto
- **Formato**: ABCD-1234-EFGH (12 caracteres alfanuméricos)
- **Hash de Verificación**: Almacenado en BD para validación
- **Persistencia**: Un código por docente (se reutiliza en regeneraciones)
- **QR Codes**: Apuntan a URL pública de verificación

## 🐛 Solución de Problemas

### Error: "Import 'docx2pdf' could not be resolved"

En macOS/Linux, instalar LibreOffice:
```bash
brew install libreoffice  # macOS con Homebrew
```

En Windows, la conversión usará Microsoft Word si está instalado.

### Error de conexión a PostgreSQL

Verificar:
1. PostgreSQL está corriendo: `pg_isready`
2. Base de datos existe: `psql -l | grep emi_certificacion`
3. Credenciales en `.env` son correctas

### Error al generar certificados

Verificar:
1. Archivo `MODELO_1_CERTIFICACION DE PRODUCCIÓN INTELECTUAL Y CIENTÍFICA.docx` existe
2. Carpeta `app/static/qr_codes/` existe y tiene permisos de escritura
3. LibreOffice o Word están instalados

## 📊 Base de Datos

**Tablas principales:**
- `usuarios` - Administradores del sistema
- `unidades_academicas` - 5 unidades de la EMI
- `docentes` - Registro de docentes
- `tipos_criterios` - 10 tipos de criterios predefinidos
- `docentes_criterios` - Relación docente-criterio con detalles
- `certificados` - Certificados generados (uno por docente)

## 🤝 Contribuir

Este es un sistema interno de la EMI. Para modificaciones o mejoras, contactar al administrador del sistema.

## 📄 Licencia

Sistema de uso interno de la Escuela Militar de Ingeniería - Bolivia.

## 👨‍💻 Desarrollador

Sistema desarrollado para la Escuela Militar de Ingeniería (EMI) - Bolivia

---

**Escuela Militar de Ingeniería**  
Sistema de Certificación de Producción Intelectual y Científica  
2025
