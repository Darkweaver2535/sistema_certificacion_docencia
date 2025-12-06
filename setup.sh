#!/bin/bash

# Script de inicialización rápida del Sistema de Certificación EMI

echo "==================================================="
echo "Sistema de Certificación Docente EMI"
echo "Script de Inicialización"
echo "==================================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}[1/7]${NC} Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar PostgreSQL
echo -e "${YELLOW}[2/7]${NC} Verificando PostgreSQL..."
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓${NC} PostgreSQL encontrado"
else
    echo -e "${RED}✗${NC} PostgreSQL no está instalado. Por favor instálalo primero."
    exit 1
fi

# Crear entorno virtual
echo -e "${YELLOW}[3/7]${NC} Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${GREEN}✓${NC} Entorno virtual ya existe"
fi

# Activar entorno virtual
echo -e "${YELLOW}[4/7]${NC} Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Entorno virtual activado"

# Instalar dependencias
echo -e "${YELLOW}[5/7]${NC} Instalando dependencias..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencias instaladas"

# Verificar archivo .env
echo -e "${YELLOW}[6/7]${NC} Verificando configuración..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}!${NC} Archivo .env no encontrado. Creando desde .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}!${NC} IMPORTANTE: Edita el archivo .env con tus credenciales de PostgreSQL"
    echo -e "${YELLOW}!${NC} Presiona ENTER cuando hayas editado el archivo .env..."
    read
fi
echo -e "${GREEN}✓${NC} Configuración verificada"

# Crear base de datos
echo -e "${YELLOW}[7/7]${NC} Configurando base de datos..."
echo -e "${YELLOW}?${NC} ¿Deseas crear la base de datos PostgreSQL ahora? (s/n)"
read -r response
if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
    echo "Ingresa tu contraseña de PostgreSQL cuando se solicite:"
    psql -U postgres -c "CREATE DATABASE emi_certificacion;" 2>/dev/null || echo -e "${YELLOW}!${NC} La base de datos ya existe o hubo un error"
    echo -e "${GREEN}✓${NC} Base de datos configurada"
fi

echo ""
echo "==================================================="
echo -e "${GREEN}Inicialización completada!${NC}"
echo "==================================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Edita el archivo .env con tus credenciales si aún no lo has hecho"
echo "2. Ejecuta: flask init-db"
echo "3. Ejecuta: flask seed-data"
echo "4. Ejecuta: flask create-admin"
echo "5. Ejecuta: python run.py"
echo ""
echo "Luego accede a: http://localhost:5000"
echo ""
