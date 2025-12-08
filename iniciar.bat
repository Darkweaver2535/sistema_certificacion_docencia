@echo off
REM Script de inicio para Sistema de Certificación EMI - Windows
REM Este script inicia el servidor y abre el navegador automáticamente

echo ========================================
echo   Sistema de Certificacion EMI
echo   Escuela Militar de Ingenieria
echo ========================================
echo.

REM Verificar que el ejecutable existe
if not exist "SistemaCertificacionEMI.exe" (
    echo ERROR: No se encuentra el archivo SistemaCertificacionEMI.exe
    echo Por favor, asegurese de ejecutar este script desde la carpeta correcta.
    pause
    exit /b 1
)

REM Verificar el archivo .env
if not exist ".env" (
    echo ADVERTENCIA: No se encuentra el archivo .env
    echo Creando archivo de configuracion por defecto...
    echo.
    (
        echo SECRET_KEY=emi-secret-key-production-2025
        echo FLASK_ENV=production
    ) > .env
    echo Archivo .env creado.
    echo El sistema usara SQLite como base de datos.
    echo.
)

echo Iniciando el Sistema de Certificacion...
echo.
echo Por favor, espere mientras el servidor se inicia...
echo Una vez iniciado, se abrira automaticamente en su navegador.
echo.

REM Iniciar el servidor en segundo plano
start /B SistemaCertificacionEMI.exe

REM Esperar 5 segundos para que el servidor inicie
timeout /t 5 /nobreak > nul

REM Abrir el navegador
echo Abriendo el navegador...
start http://localhost:5001

echo.
echo ========================================
echo   Sistema iniciado correctamente
echo ========================================
echo.
echo Acceda al sistema en: http://localhost:5001
echo Usuario por defecto: admin
echo Contraseña por defecto: admin123
echo.
echo Para detener el servidor, cierre esta ventana
echo o presione Ctrl+C
echo.
echo ========================================

REM Mantener la ventana abierta
pause
