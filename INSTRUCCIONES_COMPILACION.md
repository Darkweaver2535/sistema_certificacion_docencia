# Instrucciones para Generar el Ejecutable de Windows
## Sistema de Certificación EMI

### IMPORTANTE: Este proceso debe realizarse en una computadora con Windows

## Opción 1: Construcción Automática con GitHub Actions (Recomendado)

Ya está configurado en el repositorio. Solo necesita:

1. Hacer push a la rama `simple`
2. El ejecutable se generará automáticamente
3. Descargarlo desde la sección "Actions" de GitHub

## Opción 2: Construcción Manual en Windows

### Requisitos
- Windows 10 o superior
- Python 3.11 o superior
- Git instalado

### Pasos

1. **Clonar el repositorio**
```cmd
git clone https://github.com/Darkweaver2535/sistema_certificacion_docencia.git
cd sistema_certificacion_docencia
git checkout simple
```

2. **Crear entorno virtual**
```cmd
python -m venv venv
venv\Scripts\activate
```

3. **Instalar dependencias**
```cmd
pip install -r requirements.txt
pip install pyinstaller
```

4. **Generar el ejecutable**
```cmd
pyinstaller sistema_certificacion.spec
```

5. **El ejecutable estará en:**
```
dist\SistemaCertificacionEMI.exe
```

### Crear Paquete de Distribución

1. **Crear carpeta de distribución**
```cmd
mkdir distribucion
```

2. **Copiar archivos necesarios**
```cmd
copy dist\SistemaCertificacionEMI.exe distribucion\
copy .env.example distribucion\.env
copy INSTALACION_WINDOWS.md distribucion\
copy iniciar.bat distribucion\
xcopy app\static\emi_logo.png distribucion\ /Y
```

3. **Crear archivo README en la distribución**
Crear `distribucion\LEEME.txt` con:
```
SISTEMA DE CERTIFICACION - ESCUELA MILITAR DE INGENIERIA

1. Instale PostgreSQL si no lo tiene
2. Cree una base de datos llamada 'certificacion_emi'
3. Edite el archivo .env con sus credenciales
4. Haga doble clic en iniciar.bat
5. El sistema se abrirá en http://localhost:5001

Usuario: admin
Contraseña: admin123

Lea INSTALACION_WINDOWS.md para más detalles.
```

4. **Comprimir todo**
```cmd
powershell Compress-Archive -Path distribucion\* -DestinationPath SistemaCertificacionEMI_v1.0.zip
```

### Resultado Final

Tendrá un archivo `SistemaCertificacionEMI_v1.0.zip` que contiene:
- SistemaCertificacionEMI.exe (ejecutable principal)
- .env (archivo de configuración)
- iniciar.bat (script de inicio rápido)
- INSTALACION_WINDOWS.md (manual de instalación)
- LEEME.txt (instrucciones rápidas)

### Notas Importantes

1. **Tamaño del ejecutable:** Aproximadamente 50-80 MB
2. **Antivirus:** Algunos antivirus pueden marcar el ejecutable como sospechoso (falso positivo)
3. **Requisito:** PostgreSQL debe estar instalado en la máquina del usuario
4. **Portabilidad:** El ejecutable NO incluye PostgreSQL, solo la aplicación Flask

### Prueba del Ejecutable

1. En una máquina Windows limpia (sin Python)
2. Instale PostgreSQL
3. Cree la base de datos
4. Ejecute iniciar.bat
5. Verifique que funcione correctamente

### Distribución

El archivo ZIP puede ser distribuido a los usuarios finales.
Incluya siempre el manual INSTALACION_WINDOWS.md

---
**Nota:** Si está en macOS/Linux, use una máquina virtual Windows o GitHub Actions para compilar.
