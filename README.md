# Sistema de Certificación de Docentes - EMI Bolivia

Sistema web para la gestión y certificación de la producción intelectual y científica de docentes de la Escuela Militar de Ingeniería (EMI).

## 🎯 Características

- ✅ Gestión completa de docentes (CRUD, importación masiva desde Excel)
- ✅ 10 criterios de producción intelectual y científica
- ✅ Generación automática de certificados en PDF y Word
- ✅ Códigos QR para verificación pública de autenticidad
- ✅ Sistema de verificación pública de certificados
- ✅ 5 unidades académicas preconfiguradas
- ✅ Diseño institucional con colores EMI (azul, blanco, amarillo)
- ✅ Compatible con servidores Linux (Render, Heroku, etc.)

## 🚀 Despliegue Rápido

### Opción 1: SQLite (Recomendado para empezar) ⚡

**La forma más rápida y simple de desplegar:**

1. Crear Web Service en Render
2. Configurar Start Command: `gunicorn run:app`
3. ¡Listo!

👉 **[Ver guía completa: DEPLOYMENT_SQLITE.md](DEPLOYMENT_SQLITE.md)**

**Ventajas:**
- ✅ Configuración en 5 minutos
- ✅ Sin costos adicionales
- ✅ Base de datos se inicializa automáticamente
- ✅ Ideal para demos y pruebas

**Desventajas:**
- ⚠️ Datos se pierden en reinicio (Render Free tier)
- ⚠️ No recomendado para producción real

---

### Opción 2: PostgreSQL (Para producción) 🏢

**Para datos persistentes y uso en producción:**

1. Crear base de datos PostgreSQL en Render
2. Configurar DATABASE_URL
3. Crear Web Service
4. Inicializar base de datos

👉 **[Ver guía completa: DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md)**

**Ventajas:**
- ✅ Datos persisten entre reinicios
- ✅ Más robusto para producción
- ✅ Mejor rendimiento con muchos usuarios

**Desventajas:**
- ⚠️ Configuración más compleja
- ⚠️ Requiere plan de pago o DB externa

---

## 💻 Desarrollo Local

### Requisitos

- Python 3.10 o superior
- pip

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Darkweaver2535/sistema_certificacion_docencia.git
cd sistema_certificacion_docencia

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python init_db.py

# Ejecutar servidor de desarrollo
python run.py
```

Abre tu navegador en `http://localhost:5000`

**Login inicial:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ Cambia la contraseña después del primer login

---

## 📁 Estructura del Proyecto

```
sistema_certificacion_docentes/
├── app/
│   ├── blueprints/          # Rutas de la aplicación
│   │   ├── auth.py          # Autenticación
│   │   ├── certificados.py  # Gestión de certificados
│   │   ├── criterios.py     # Gestión de criterios
│   │   ├── docentes.py      # Gestión de docentes
│   │   └── public.py        # Rutas públicas (verificación)
│   ├── models/              # Modelos de base de datos
│   ├── static/              # CSS, JavaScript, imágenes
│   │   ├── css/
│   │   │   └── emi-style.css  # Estilos institucionales EMI
│   │   ├── images/
│   │   └── qr_codes/        # Códigos QR generados
│   ├── templates/           # Plantillas HTML
│   └── utils/               # Utilidades (generador de certificados)
├── config.py                # Configuración de la aplicación
├── run.py                   # Punto de entrada
├── init_db.py              # Script de inicialización de BD
├── requirements.txt         # Dependencias Python
├── DEPLOYMENT_SQLITE.md    # Guía de despliegue con SQLite
└── DEPLOYMENT_RENDER.md    # Guía de despliegue con PostgreSQL
```

---

## 🎨 Diseño Institucional EMI

El sistema utiliza la paleta de colores oficial de la EMI:

- **Azul Oscuro**: `#003366` - Encabezados principales, navbar
- **Azul EMI**: `#0066cc` - Botones, enlaces, acentos
- **Amarillo EMI**: `#FFD700` - Advertencias, highlights
- **Blanco**: `#FFFFFF` - Fondos, tarjetas

Todos los componentes siguen el diseño institucional para mantener coherencia visual.

---

## 📋 Criterios de Certificación

El sistema incluye 10 criterios predefinidos:

1. Libros publicados
2. Artículos en revistas indexadas
3. Capítulos de libros
4. Ponencias en congresos
5. Proyectos de investigación
6. Tesis dirigidas
7. Patentes o registros
8. Premios y reconocimientos
9. Formación académica avanzada
10. Participación en redes académicas

---

## 🏢 Unidades Académicas

Preconfiguradas:

- La Paz
- Cochabamba
- Santa Cruz
- Oruro
- Sucre

---

## 📄 Generación de Certificados

### Proceso

1. **Generar Word (.docx)** con datos del docente
2. **Convertir a HTML** usando `mammoth`
3. **Convertir a PDF** usando `weasyprint`
4. **Insertar código QR** para verificación

### Formatos disponibles

- **PDF** (conversión automática, compatible con Linux)
- **Word** (documento original editable)

### Template

El sistema requiere un archivo Word template con placeholders:
- `{{CODIGO}}` - Código único
- `{{NOMBRE}}` - Nombre completo
- `{{CI}}` - Cédula de identidad
- `{{UNIDAD}}` - Unidad académica
- `{{CIUDAD}}` - Ciudad
- `{{FECHA}}` - Fecha de emisión
- `{{QR}}` - Código QR
- `{{CRITERIOS}}` - Lista de criterios

---

## 🔐 Seguridad

- Autenticación con Flask-Login
- Contraseñas hasheadas con Werkzeug
- Códigos únicos con HMAC-SHA256
- HTTPS automático en Render
- Verificación pública sin autenticación

---

## 🛠️ Tecnologías

**Backend:**
- Flask 3.0
- SQLAlchemy (ORM)
- PostgreSQL / SQLite
- Gunicorn (WSGI server)

**Frontend:**
- Bootstrap 5
- Bootstrap Icons
- CSS Grid/Flexbox
- Vanilla JavaScript

**Generación de Documentos:**
- python-docx (Word)
- mammoth (DOCX → HTML)
- weasyprint (HTML → PDF)
- qrcode (Códigos QR)

---

## 📞 Soporte

**Desarrollado por:** Alvaro Santiago Encinas Flores  
**WhatsApp:** +591 76260216  
**GitHub:** [@Darkweaver2535](https://github.com/Darkweaver2535)

---

## 📄 Licencia

Este proyecto fue desarrollado específicamente para la Escuela Militar de Ingeniería (EMI) Bolivia.

---

## 🎯 Estado del Proyecto

✅ **Versión 1.0 - Producción**

- Sistema completamente funcional
- Diseño institucional EMI implementado
- Compatible con servidores Linux
- Listo para despliegue en Render.com

---

## 🚀 Próximas Mejoras

- [ ] Dashboard con estadísticas
- [ ] Exportación masiva de certificados
- [ ] Sistema de notificaciones por email
- [ ] API REST para integraciones
- [ ] Panel de administración avanzado
- [ ] Reportes y gráficas

---

**¡Gracias por usar el Sistema de Certificación EMI!** 🎓
