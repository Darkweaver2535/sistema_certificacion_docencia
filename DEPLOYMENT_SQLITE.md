# Guía Rápida de Despliegue en Render.com (SQLite)

## ✅ Configuración Simplificada con SQLite

El sistema está configurado para usar **SQLite** por defecto, lo que elimina la necesidad de configurar una base de datos PostgreSQL externa. ¡Mucho más rápido y simple! 🚀

---

## 📋 Pasos para Desplegar (3 pasos simples)

### 1. Crear Web Service en Render

1. Ve a tu [Dashboard de Render](https://dashboard.render.com/)
2. Haz click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub: `Darkweaver2535/sistema_certificacion_docencia`
4. Configura:
   - **Name**: `sistema-certificacion-emi`
   - **Region**: Oregon (USA) - o la más cercana a ti
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free

### 2. Configurar Variables de Entorno (OPCIONAL)

En la sección **"Environment"** del Web Service, puedes agregar (pero no es obligatorio):

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | (generar clave aleatoria)* | Clave secreta de Flask (recomendado para producción) |
| `CERTIFICATE_SALT` | (generar salt aleatorio)* | Salt para códigos únicos (recomendado para producción) |

**Generar claves aleatorias (opcional):**

En tu terminal local ejecuta:

```bash
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32)); print('CERTIFICATE_SALT:', secrets.token_hex(16))"
```

Si no configuras estas variables, el sistema usará valores por defecto (funcionará, pero es menos seguro).

### 3. ¡Listo! Espera el Deploy

1. Haz click en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Verás los logs en tiempo real
4. Cuando veas **"Build successful"** y el servicio esté **"Live"**, ya está listo

---

## 🎯 Primera Vez que Accedes

### La base de datos se inicializa automáticamente

Cuando accedas por primera vez a tu aplicación:

1. Ve a la URL de tu aplicación (ej: `https://sistema-certificacion-emi.onrender.com`)
2. El sistema detectará que no hay base de datos y la creará automáticamente
3. Se crearán:
   - ✅ Usuario administrador: `admin` / `admin123`
   - ✅ 5 Unidades Académicas (La Paz, Cochabamba, Santa Cruz, Oruro, Sucre)
   - ✅ 10 Criterios de Certificación
4. Inicia sesión con: **usuario**: `admin`, **contraseña**: `admin123`
5. ⚠️ **IMPORTANTE**: Cambia la contraseña inmediatamente después del primer login

---

## 📁 ¿Dónde están los Datos?

- **Base de datos**: `emi_certificacion.db` (SQLite) en el directorio del proyecto
- **QR Codes**: `app/static/qr_codes/`
- **Certificados**: `app/static/qr_codes/` (junto con los QR)
- **Importaciones**: `uploads/importaciones/`

⚠️ **IMPORTANTE en Render Free Tier**: Los archivos en el sistema se borran cuando el servicio se reinicia. Para persistencia de datos, considera:
- Usar un plan de pago de Render con disco persistente
- O migrar a PostgreSQL (más complejo pero los datos persisten)

---

## 🔧 Subir Template de Certificado

El sistema necesita un archivo Word como template. Tienes dos opciones:

### Opción A: Incluirlo en el Repositorio (Recomendado)

1. En tu computadora, copia el archivo template a la raíz del proyecto
2. Renómbralo exactamente a: `MODELO_1_CERTIFICACION DE PRODUCCIÓN INTELECTUAL Y CIENTÍFICA.docx`
3. Ejecuta:
```bash
git add "MODELO_1_CERTIFICACION DE PRODUCCIÓN INTELECTUAL Y CIENTÍFICA.docx"
git commit -m "Agregar template de certificado"
git push origin main
```
4. Render detectará el cambio y re-desplegará automáticamente

### Opción B: Actualizar la Ruta en config.py

Si tu template tiene otro nombre o está en otra ubicación, edita `config.py`:

```python
CERTIFICATE_TEMPLATE = os.path.join(BASE_DIR, 'tu_template.docx')
```

---

## 📦 Formatos de Descarga

El sistema ofrece dos formatos:

- **PDF**: Convertido automáticamente desde Word (compatible con Linux/Render)
- **Word (.docx)**: Documento original editable

Si la conversión a PDF falla, el sistema descargará automáticamente el archivo Word.

---

## 🐛 Solución de Problemas

### Error: "Application failed to start"
**Solución**: 
1. Ve a **"Logs"** en el Dashboard de Render
2. Busca el error específico
3. Generalmente es por falta de alguna dependencia o error en el código

### Error: "Template no encontrado"
**Solución**: Sube el archivo template como se indica arriba

### La aplicación se reinicia sola
**Comportamiento normal**: Render reinicia servicios gratuitos después de 15 minutos de inactividad. La base de datos se recreará automáticamente.

### Quiero que los datos persistan entre reinicios
**Solución**: 
- **Opción 1**: Actualizar a un plan de pago de Render con disco persistente
- **Opción 2**: Usar PostgreSQL (sigue la guía en `DEPLOYMENT_RENDER.md`)

---

## 🔒 Seguridad Post-Despliegue

1. ✅ **Cambiar contraseña del admin** (en la aplicación, después del primer login)
2. ✅ **Configurar SECRET_KEY personalizada** (en Environment Variables)
3. ✅ **Configurar CERTIFICATE_SALT personalizado** (en Environment Variables)
4. ✅ **HTTPS automático** (Render lo proporciona gratis)
5. ✅ **Dominio personalizado** (opcional, configurable en Render)

---

## 📊 Comparación: SQLite vs PostgreSQL

| Característica | SQLite (Actual) | PostgreSQL |
|----------------|-----------------|------------|
| **Configuración** | ✅ Muy simple | ⚠️ Compleja |
| **Costo** | ✅ Gratis | ⚠️ Requiere plan pago o DB externa |
| **Persistencia** | ⚠️ Se pierde en reinicio (Render Free) | ✅ Datos persisten |
| **Velocidad inicial** | ✅ Muy rápida | ⚠️ Más lenta |
| **Ideal para** | ✅ Pruebas, demos, prototipos | ✅ Producción real |

---

## 🎯 URLs Importantes

- **Dashboard Render**: https://dashboard.render.com/
- **Documentación Render**: https://render.com/docs
- **Repositorio GitHub**: https://github.com/Darkweaver2535/sistema_certificacion_docencia

---

## 📞 Soporte

Desarrollado por: **Alvaro Santiago Encinas Flores**  
WhatsApp: **+591 76260216**

---

## 🚀 ¡Todo Listo!

Con SQLite, el despliegue es **muchísimo más rápido**:
1. Crear Web Service
2. (Opcional) Configurar SECRET_KEY
3. ¡Listo!

No necesitas Shell, no necesitas inicializar base de datos manualmente, no necesitas PostgreSQL. El sistema lo hace todo automáticamente. 🎉
