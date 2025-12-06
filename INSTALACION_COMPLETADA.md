# ✅ Instalación Completada

## 🎉 Todas las dependencias están instaladas correctamente

### Próximos Pasos

#### 1️⃣ Configurar PostgreSQL

```bash
# Iniciar PostgreSQL (si no está corriendo)
brew services start postgresql@14

# O si usas otra versión:
# brew services start postgresql

# Crear la base de datos
createdb emi_certificacion

# O manualmente:
psql postgres
CREATE DATABASE emi_certificacion;
\q
```

#### 2️⃣ Configurar Variables de Entorno

El archivo `.env` ya está creado. **Edítalo con tus credenciales**:

```bash
nano .env
```

Actualiza la línea `DATABASE_URL` con tu contraseña de PostgreSQL:
```
DATABASE_URL=postgresql://postgres:TU_PASSWORD_AQUI@localhost:5432/emi_certificacion
```

Guarda: `Ctrl+O`, luego `Enter`, y sal: `Ctrl+X`

#### 3️⃣ Inicializar Base de Datos

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate

# Crear tablas
flask init-db

# Poblar datos iniciales (5 unidades + 10 criterios)
flask seed-data

# Crear usuario administrador
flask create-admin
```

Cuando ejecutes `flask create-admin`, ingresa:
- Username: `admin` (o el que prefieras)
- Password: (tu contraseña segura)
- Nombre completo: `Administrador EMI`
- Email: `admin@emi.edu.bo`

#### 4️⃣ Ejecutar el Sistema

```bash
python run.py
```

El sistema estará disponible en: **http://localhost:5000**

---

## 🔐 Primer Login

1. Abre tu navegador en: `http://localhost:5000`
2. Serás redirigido a `/auth/login`
3. Ingresa las credenciales del admin
4. ¡Listo! Accederás al Dashboard

---

## 📝 Comandos Útiles

```bash
# Ver todas las rutas
flask routes

# Abrir shell interactivo
flask shell

# Reiniciar base de datos (⚠️ BORRA TODO)
flask init-db

# Regenerar seeds
flask seed-data
```

---

## 🧪 Probar el Sistema

### 1. Registrar un Docente de Prueba

- Dashboard → Nuevo Docente
- Completar datos:
  - Nombres: Juan
  - Apellidos: Pérez López
  - CI: 12345678
  - Unidad: UALP - La Paz
  - Cargo: Docente Titular
  - Años de servicio: 10
  - Email: juan.perez@emi.edu.bo
  - Teléfono: 70123456

### 2. Agregar Criterios

- Docentes → Ver docente → Gestionar Criterios
- Marcar 2-3 criterios de ejemplo
- Agregar detalles (ej: "Congreso Internacional XYZ, 2024")
- Guardar

### 3. Generar Certificado

- Ver docente → Generar Certificado
- Se descargará un PDF automáticamente
- El PDF tendrá código único y QR

### 4. Verificar con QR

- Escanear el QR del certificado
- Se abrirá `/verificar/XXXX-XXXX-XXXX`
- Verás los datos del docente sin autenticación

---

## 🛠️ Solución de Problemas

### PostgreSQL no conecta

```bash
# Verificar que está corriendo
pg_isready

# Si no está corriendo, iniciarlo
brew services start postgresql@14
```

### Error "relation does not exist"

```bash
# Recrear tablas
flask init-db
flask seed-data
```

### Puerto 5000 ocupado

En `run.py`, cambiar:
```python
app.run(debug=True, port=5001)
```

### docx2pdf no funciona

Instalar LibreOffice:
```bash
brew install libreoffice
```

---

## 📦 Estructura Final

```
sistema_de_certificacion_docentes/
├── app/                     # Aplicación Flask
│   ├── blueprints/          # Rutas (auth, docentes, criterios, certificados, public)
│   ├── models/              # Modelos de BD
│   ├── templates/           # Templates HTML
│   ├── static/              # CSS, JS, QR codes
│   └── utils/               # Generador de certificados
├── uploads/                 # Importaciones Excel/CSV
├── venv/                    # Entorno virtual ✅
├── run.py                   # Punto de entrada
├── config.py                # Configuración
├── requirements.txt         # Dependencias ✅
├── .env                     # Variables de entorno
└── README.md                # Documentación completa
```

---

## ✅ Checklist Final

- [✅] Python 3.13 instalado
- [✅] Entorno virtual creado (venv)
- [✅] Dependencias instaladas
- [✅] Archivos .env creado
- [ ] PostgreSQL configurado
- [ ] Base de datos creada
- [ ] Tablas inicializadas (`flask init-db`)
- [ ] Datos iniciales cargados (`flask seed-data`)
- [ ] Usuario admin creado (`flask create-admin`)
- [ ] Sistema ejecutándose

---

**¡El sistema está listo para usar!** 🚀

Solo falta configurar PostgreSQL y ejecutar los comandos de inicialización.

---

**Sistema de Certificación EMI - 2025**  
Desarrollado con Flask, PostgreSQL, Bootstrap 5
