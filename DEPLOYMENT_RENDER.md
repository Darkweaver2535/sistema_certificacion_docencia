# Guía de Despliegue en Render.com

## ✅ Cambios Implementados para Linux

El sistema ha sido modificado para funcionar correctamente en servidores Linux (como Render.com):

### Conversión de Certificados (Word → PDF)

- **Antes**: Usaba `docx2pdf` que requiere Microsoft Word (solo Windows/Mac)
- **Ahora**: Usa `weasyprint` + `mammoth` compatible con Linux
- **Proceso**:
  1. Se genera el documento Word (.docx) con todos los datos
  2. Se convierte Word → HTML usando `mammoth`
  3. Se convierte HTML → PDF usando `weasyprint`
  4. El usuario puede descargar tanto Word como PDF

### Servidor de Producción

- **Antes**: Flask development server (solo para desarrollo)
- **Ahora**: Gunicorn WSGI server (listo para producción)
- **Puerto**: Lee automáticamente `PORT` del entorno (requerido por Render)

---

## 📋 Pasos para Desplegar en Render.com

### 1. Crear PostgreSQL Database

1. Ve a tu [Dashboard de Render](https://dashboard.render.com/)
2. Haz click en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `certificacion-db`
   - **Database**: `certificacion_docentes`
   - **User**: (generado automáticamente)
   - **Region**: Oregon (USA) - o la más cercana
   - **Plan**: Free
4. Haz click en **"Create Database"**
5. **IMPORTANTE**: Copia el **"Internal Database URL"** (se ve como `postgresql://usuario:password@dpg-...`)

### 2. Crear Web Service

1. En el Dashboard, haz click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub: `Darkweaver2535/sistema_certificacion_docencia`
3. Configura:
   - **Name**: `sistema-certificacion-emi`
   - **Region**: Oregon (USA) - **debe ser la misma que la base de datos**
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free

### 3. Configurar Variables de Entorno

⚠️ **MUY IMPORTANTE**: Render usa URLs con formato `postgres://` pero SQLAlchemy 1.4+ requiere `postgresql://`. El sistema convierte automáticamente, pero debes copiar la URL exactamente como Render te la proporciona.

En la sección **"Environment"** del Web Service, agrega estas variables:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `DATABASE_URL` | (pegar **Internal Database URL** exactamente como aparece en Render) | URL de conexión a PostgreSQL - **copiar textualmente** |
| `SECRET_KEY` | (generar clave aleatoria)* | Clave secreta de Flask |
| `FLASK_APP` | `run.py` | Archivo principal de la app |
| `FLASK_ENV` | `production` | Ambiente de producción |
| `CERTIFICATE_SALT` | (generar salt aleatorio)* | Salt para códigos únicos |

**📝 Cómo obtener la Internal Database URL:**

1. Ve a tu PostgreSQL database en Render
2. En la sección **"Connections"**, copia la **"Internal Database URL"**
3. Se verá algo como: `postgres://user:password@dpg-xxxxx.oregon-postgres.render.com/dbname`
4. **Pégala TAL CUAL en DATABASE_URL** (el sistema la convertirá automáticamente a `postgresql://`)

**Generar claves aleatorias seguras:**

En tu terminal local ejecuta:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copia el resultado y úsalo para `SECRET_KEY` y `CERTIFICATE_SALT`

### 4. Verificar Configuración

Antes de inicializar la base de datos, verifica que todo esté configurado correctamente:

1. Ve a **"Shell"** en el Dashboard de Render
2. Ejecuta el script de verificación:

```bash
python verify_config.py
```

Este script verificará:
- ✅ Variables de entorno configuradas
- ✅ Formato correcto de DATABASE_URL
- ✅ Conexión a la base de datos
- ✅ Carpetas del sistema
- ✅ Template de certificado

Si todas las verificaciones pasan, continúa con el paso 5. Si hay errores, corrígelos antes de continuar.

### 5. Inicializar Base de Datos

Una vez que el servicio esté desplegado **Y las verificaciones pasen**:

1. Ve a **"Shell"** en el Dashboard de Render
2. Ejecuta estos comandos:

```bash
# Entrar a Python
python

# Ejecutar comandos de inicialización
from app import create_app, db
from app.models.usuario import Usuario
from app.models.unidad_academica import UnidadAcademica
from app.models.tipo_criterio import TipoCriterio

app = create_app()
with app.app_context():
    # Crear todas las tablas
    db.create_all()
    
    # Crear usuario admin
    admin = Usuario(username='admin', nombre_completo='Administrador EMI')
    admin.set_password('admin123')  # CAMBIAR ESTA CONTRASEÑA
    db.session.add(admin)
    
    # Crear unidades académicas de ejemplo
    unidades = [
        UnidadAcademica(codigo='UNI-LA-PAZ', nombre='Unidad Académica La Paz', ciudad='La Paz'),
        UnidadAcademica(codigo='UNI-CBBA', nombre='Unidad Académica Cochabamba', ciudad='Cochabamba'),
        UnidadAcademica(codigo='UNI-SCZ', nombre='Unidad Académica Santa Cruz', ciudad='Santa Cruz'),
        UnidadAcademica(codigo='UNI-ORURO', nombre='Unidad Académica Oruro', ciudad='Oruro'),
        UnidadAcademica(codigo='UNI-SUCRE', nombre='Unidad Académica Sucre', ciudad='Sucre'),
    ]
    db.session.add_all(unidades)
    
    # Crear criterios de certificación
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
    
    # Guardar todos los cambios
    db.session.commit()
    print("✅ Base de datos inicializada correctamente")

# Salir de Python
exit()
```

### 5. Subir Template de Certificado

El sistema necesita un archivo Word como template en `templates/certificado_template.docx`:

1. Desde el Shell de Render, crear la carpeta:
```bash
mkdir -p templates
```

2. **IMPORTANTE**: Debes subir tu archivo `certificado_template.docx` al servidor. Opciones:

   **Opción A: Incluirlo en el repositorio** (Recomendado)
   - Agrega el archivo a tu repositorio local
   - Commit y push a GitHub
   - Render lo descargará automáticamente

   **Opción B: Usar almacenamiento persistente de Render**
   - Configurar un Disk Mount en Render
   - Subir el archivo manualmente

### 6. Verificar Despliegue

1. Espera a que el build termine (verás "Build successful" en los logs)
2. Abre la URL de tu aplicación (algo como `https://sistema-certificacion-emi.onrender.com`)
3. Prueba el login con: `admin` / `admin123` (o la contraseña que estableciste)
4. ⚠️ **IMPORTANTE**: Cambia la contraseña del admin inmediatamente

---

## 🔧 Configuración del Template de Certificado

El archivo `certificado_template.docx` debe contener estos placeholders:

- `{{CODIGO}}` - Código único del certificado
- `{{NOMBRE}}` - Nombre completo del docente
- `{{CI}}` - Cédula de identidad
- `{{UNIDAD}}` - Nombre de la unidad académica
- `{{CIUDAD}}` - Ciudad de la unidad
- `{{CARGO}}` - Cargo del docente
- `{{FECHA}}` - Fecha de emisión
- `{{QR}}` - Código QR (se insertará automáticamente)
- `{{CRITERIOS}}` - Lista de criterios (se insertará automáticamente)

---

## 📦 Formatos de Descarga

El sistema ahora ofrece dos formatos de descarga:

- **PDF**: Convertido automáticamente desde Word
- **Word (.docx)**: Documento original editable

Si la conversión a PDF falla en el servidor, el sistema automáticamente descargará el archivo Word.

---

## 🐛 Solución de Problemas

### Error: "connection to server at localhost refused"
**Causa**: DATABASE_URL no está configurada o no se está leyendo correctamente.

**Solución**: 
1. Verifica que DATABASE_URL esté en las Environment Variables de Render
2. Copia la **Internal Database URL** exactamente desde tu PostgreSQL database
3. Pégala en DATABASE_URL sin modificarla (se convertirá automáticamente)
4. Reinicia el Web Service
5. Ejecuta `python verify_config.py` en el Shell para verificar

### Error: "No open HTTP ports detected"
**Solución**: Asegúrate de que el Start Command sea exactamente: `gunicorn run:app`

### Error de Base de Datos
**Solución**: Verifica que `DATABASE_URL` esté configurada correctamente y que la región del Web Service y la Database sean la misma.

### Error al generar PDF
**Solución**: El sistema automáticamente descargará el archivo Word si la conversión falla. Esto es normal en el primer despliegue.

### Logs de Render
Para ver errores detallados, ve a **"Logs"** en el Dashboard de tu Web Service.

---

## 🔒 Seguridad Post-Despliegue

1. **Cambiar contraseña del admin**
2. **Generar nuevas claves** para `SECRET_KEY` y `CERTIFICATE_SALT`
3. **Configurar dominio personalizado** (opcional)
4. **Habilitar HTTPS** (Render lo hace automáticamente)
5. **Configurar backups** de la base de datos

---

## 📞 Soporte

Desarrollado por: Alvaro Santiago Encinas Flores
WhatsApp: +591 76260216

---

## 🎯 URLs Importantes

- **Dashboard Render**: https://dashboard.render.com/
- **Documentación Render**: https://render.com/docs
- **Repositorio GitHub**: https://github.com/Darkweaver2535/sistema_certificacion_docencia
