#!/bin/bash

# Script para configurar Google Gemini API
# Asesor PyME Inteligente

set -e

echo "🔑 Configurando Google Gemini API..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se proporcionó API key
if [ -z "$1" ]; then
    print_error "Por favor proporciona tu API key de Google Gemini:"
    echo "Uso: ./setup-gemini.sh YOUR_GEMINI_API_KEY"
    echo ""
    echo "Para obtener tu API key:"
    echo "1. Ve a https://makersuite.google.com/app/apikey"
    echo "2. Crea una nueva API key"
    echo "3. Copia la key y úsala con este script"
    exit 1
fi

GEMINI_API_KEY=$1

print_status "Configurando API key de Google Gemini..."

# Actualizar archivo .env
if [ -f ".env" ]; then
    sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$GEMINI_API_KEY/" .env
else
    echo "GEMINI_API_KEY=$GEMINI_API_KEY" > .env
fi

print_status "API key configurada en .env"

# Si estamos en Azure VM, actualizar también ahí
if [ ! -z "$AZURE_VM_IP" ]; then
    print_status "Actualizando configuración en Azure VM..."
    ssh -o StrictHostKeyChecking=no azureuser@$AZURE_VM_IP "cd /home/azureuser/asesor-pyme && echo 'GEMINI_API_KEY=$GEMINI_API_KEY' > .env"
    
    print_status "Reiniciando servicios en Azure VM..."
    ssh -o StrictHostKeyChecking=no azureuser@$AZURE_VM_IP "cd /home/azureuser/asesor-pyme && docker-compose restart"
fi

print_status "✅ Google Gemini API configurada exitosamente!"
print_status "🤖 El chat inteligente ahora está habilitado"

# Verificar configuración
print_status "Verificando configuración..."
if grep -q "GEMINI_API_KEY=$GEMINI_API_KEY" .env; then
    print_status "✅ API key configurada correctamente"
else
    print_error "❌ Error al configurar API key"
    exit 1
fi
