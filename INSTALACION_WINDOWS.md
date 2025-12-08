# Guía de Instalación - Sistema de Certificación EMI
## Para Windows

### Requisitos Previos
- Windows 10 o superior
- PostgreSQL 13 o superior instalado
- 100 MB de espacio en disco

### Instalación de PostgreSQL (si no está instalado)

1. Descargue PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Ejecute el instalador y siga las instrucciones
3. Durante la instalación:
   - Anote la contraseña que configure para el usuario `postgres`
   - Puerto por defecto: 5432
   - Marque la opción de instalar pgAdmin 4

### Configuración de la Base de Datos

1. Abra pgAdmin 4 o use psql
2. Cree una nueva base de datos llamada `certificacion_emi`
3. Anote los siguientes datos:
   - Host: `localhost`
   - Puerto: `5432`
   - Usuario: `postgres`
   - Contraseña: [la que configuró]
   - Base de datos: `certificacion_emi`

### Instalación del Sistema

1. **Extraer el archivo**
   - Descomprima el archivo ZIP en una carpeta de su preferencia
   - Ejemplo: `C:\SistemaCertificacionEMI`

2. **Configurar la conexión a la base de datos**
   - Abra el archivo `.env` con un editor de texto
   - Modifique la línea `DATABASE_URL` con sus datos:
   ```
   DATABASE_URL=postgresql://postgres:SU_CONTRASEÑA@localhost:5432/certificacion_emi
   ```
   - Reemplace `SU_CONTRASEÑA` con la contraseña de PostgreSQL

3. **Ejecutar el sistema**
   - Haga doble clic en `SistemaCertificacionEMI.exe`
   - La primera vez, el sistema creará las tablas automáticamente
   - Espere a que aparezca el mensaje: "Running on http://127.0.0.1:5001"

4. **Acceder al sistema**
   - Abra su navegador web (Chrome, Firefox, Edge)
   - Vaya a: `http://localhost:5001`
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

**Error: "No se puede conectar a la base de datos"**
- Verifique que PostgreSQL esté ejecutándose
- Revise el archivo `.env` y corrija los datos de conexión
- Asegúrese de que la base de datos `certificacion_emi` existe

**Error: "Puerto 5001 en uso"**
- Cierre cualquier otra instancia del programa
- O cambie el puerto en el archivo `run.py`

**El navegador no abre automáticamente**
- Abra manualmente: http://localhost:5001

### Crear Respaldos

1. Inicie sesión en el sistema
2. Vaya al Dashboard
3. En la parte inferior, pase el mouse sobre "Herramientas Avanzadas"
4. Haga clic en "Descargar Respaldo (PostgreSQL)"
5. Guarde el archivo .sql en un lugar seguro

### Restaurar desde Respaldo

1. Abra pgAdmin 4
2. Clic derecho en la base de datos `certificacion_emi`
3. Seleccione "Restore..."
4. Seleccione el archivo .sql del respaldo
5. Haga clic en "Restore"

### Soporte Técnico

Para problemas o consultas:
- Email: soporte@emi.edu.bo
- Teléfono: [Número de contacto]

---
**Versión del Sistema:** 1.0.0 (Simple)  
**Última actualización:** Diciembre 2025
