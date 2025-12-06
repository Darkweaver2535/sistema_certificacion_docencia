# 🚀 Guía de Inicio Rápido - Sistema de Certificación EMI

## Instalación en 5 Pasos

### 1️⃣ Ejecutar Script de Setup (Recomendado)

```bash
cd /Users/alvaroencinas/Desktop/sistema_de_certificacion_docentes
./setup.sh
```

### 2️⃣ Configurar Base de Datos

```bash
# Editar .env con tus credenciales de PostgreSQL
nano .env

# Inicializar base de datos
source venv/bin/activate
flask init-db
```

### 3️⃣ Poblar Datos Iniciales

```bash
# Crear las 5 unidades académicas y 10 criterios
flask seed-data
```

### 4️⃣ Crear Usuario Administrador

```bash
flask create-admin
# Seguir las instrucciones en pantalla
```

### 5️⃣ Iniciar Aplicación

```bash
python run.py
# Abrir navegador en: http://localhost:5000
```

---

## 📋 Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] PostgreSQL instalado y corriendo
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado con credenciales correctas
- [ ] Base de datos `emi_certificacion` creada
- [ ] Tablas inicializadas (`flask init-db`)
- [ ] Datos iniciales cargados (`flask seed-data`)
- [ ] Usuario admin creado (`flask create-admin`)
- [ ] Aplicación corriendo en http://localhost:5000

---

## 🔑 Primer Login

1. Ir a: `http://localhost:5000/auth/login`
2. Ingresar credenciales del admin creado
3. Acceder al Dashboard

---

## 📝 Flujo de Trabajo Típico

### Registrar un Docente

```
Dashboard → Nuevo Docente → Completar formulario → Guardar
```

### Importar Docentes Masivamente

```
Dashboard → Importar Excel → Descargar plantilla → 
Completar Excel → Subir archivo → Revisar resultados
```

### Asignar Criterios

```
Docentes → Ver docente → Gestionar Criterios → 
Marcar criterios → Agregar detalles → Guardar
```

### Generar Certificado

```
Docentes → Ver docente → Generar Certificado →
PDF descarga automáticamente con código QR
```

### Verificar Certificado

```
Escanear QR del certificado → 
Se abre http://localhost:5000/verificar/XXXX-XXXX-XXXX →
Visualizar datos del docente y criterios
```

---

## 🆘 Comandos Útiles

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar aplicación
python run.py

# Abrir shell interactivo
flask shell

# Ver rutas disponibles
flask routes

# Reiniciar base de datos (⚠️ BORRA TODO)
flask init-db
flask seed-data
flask create-admin
```

---

## 📊 Unidades Académicas Preconfiguradas

- **UALP** - Unidad Académica La Paz
- **UACB** - Unidad Académica Cochabamba
- **UASC** - Unidad Académica Santa Cruz
- **UARB** - Unidad Académica Riberalta
- **UATP** - Unidad Académica Trópico

---

## 🎯 10 Criterios de Producción Intelectual

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

---

## 🔧 Solución Rápida de Problemas

### No se conecta a PostgreSQL
```bash
# Verificar que PostgreSQL está corriendo
pg_isready

# Verificar credenciales en .env
cat .env | grep DATABASE_URL
```

### Error al importar docx2pdf
```bash
# macOS: Instalar LibreOffice
brew install libreoffice
```

### Puerto 5000 ocupado
```python
# En run.py, cambiar:
app.run(debug=True, port=5001)
```

---

## 📞 Soporte

Para problemas o consultas, contactar al administrador del sistema EMI.

---

**Sistema de Certificación EMI - 2025**
