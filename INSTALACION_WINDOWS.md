# Guía de Instalación - Sistema de Certificación EMI
## Para Windows

### Requisitos Previos
- Windows 10 o superior
- **NO requiere PostgreSQL** (usa SQLite integrado)
- **NO requiere Python** (el ejecutable lo incluye)
- 100 MB de espacio en disco

### Instalación del Sistema

1. **Extraer el archivo**
   - Descomprima el archivo ZIP en una carpeta de su preferencia
   - Ejemplo: `C:\SistemaCertificacionEMI`

2. **Configuración (OPCIONAL)**
   - El archivo `.env` ya viene configurado
   - Solo modifique si desea cambiar la clave secreta:
   ```
   SECRET_KEY=su-clave-secreta-personalizada
   ```
   - La base de datos SQLite se creará automáticamente en `emi_certificacion.db`

3. **Ejecutar el sistema**
   - Haga doble clic en `iniciar.bat`
   - La primera vez, el sistema creará las tablas automáticamente
   - Se abrirá su navegador en `http://localhost:5001`
   - **IMPORTANTE:** Mantenga abierta la ventana del terminal

4. **Acceder al sistema**
   - Usuario por defecto: `admin`
   - Contraseña por defecto: `admin123`

### Primer Uso

1. **Cambiar contraseña de administrador**
   - Es importante cambiar la contraseña por defecto inmediatamente

2. **Configurar criterios**
   - Los 10 criterios vienen pre-configurados
   - Puede editarlos desde el panel de administración si es necesario

3. **Registrar docentes**
   - Use "Registrar Docente" para agregar docentes uno por uno
   - O use "Importar desde Excel" para carga masiva

### Solución de Problemas

**El navegador no abre automáticamente**
- Abra manualmente: http://localhost:5001

**Error: "Puerto 5001 en uso"**
- Cierre cualquier otra instancia del programa
- Reinicie la computadora

**No aparece la ventana del navegador**
- Espere 10 segundos y abra Chrome/Firefox
- Vaya a: http://localhost:5001

### Crear Respaldos

**Método 1: Copiar el archivo de base de datos**
- Cierre el sistema (cierre la ventana del terminal)
- Copie el archivo `emi_certificacion.db` a un lugar seguro
- Guarde también la carpeta `app/static/qr_codes/` con los códigos QR

**Método 2: Usar la función de respaldo del sistema**
1. Inicie sesión en el sistema
2. Vaya al Dashboard
3. En la parte inferior, pase el mouse sobre "Herramientas Avanzadas"
4. Haga clic en "Descargar Respaldo"
5. Guarde el archivo .sql en un lugar seguro

### Restaurar desde Respaldo

**Si usó el Método 1:**
- Cierre el sistema
- Reemplace el archivo `emi_certificacion.db` con su copia de respaldo
- Restaure la carpeta `app/static/qr_codes/` si es necesario
- Inicie el sistema nuevamente

**Si usó el Método 2:**
- Use un visor de SQLite para importar el archivo .sql
- O contacte soporte técnico

### Soporte Técnico

Para problemas o consultas:
- Email: soporte@emi.edu.bo
- Teléfono: [Número de contacto]

---
**Versión del Sistema:** 1.0.0 (Simple)  
**Última actualización:** Diciembre 2025
