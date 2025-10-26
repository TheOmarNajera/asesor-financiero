#!/bin/bash

# Script para configurar GitHub Secrets para Azure
# Asesor PyME Inteligente - Deployment Automático

set -e

echo "🔐 Configurando GitHub Secrets para Azure Deployment"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Verificar que Azure CLI está instalado
if ! command -v az &> /dev/null; then
    print_error "Azure CLI no está instalado"
    echo "Instala desde: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Verificar que gh (GitHub CLI) está instalado
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI no está instalado"
    echo "Instala desde: https://cli.github.com/"
    echo "O configura los secrets manualmente en GitHub"
fi

print_success "Herramientas verificadas"

echo ""
echo "========================================="
echo "1. Configurando Azure Service Principal"
echo "========================================="

# Login en Azure
echo "Iniciando sesión en Azure..."
az login

# Obtener subscription ID
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "Subscription ID: $SUBSCRIPTION_ID"

# Crear Service Principal
SP_NAME="asesor-pyme-github-actions"
echo "Creando Service Principal: $SP_NAME"

SP_OUTPUT=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID" \
    --sdk-auth \
    --output json)

print_success "Service Principal creado"

echo ""
echo "========================================="
echo "2. Configurando GitHub Secrets"
echo "========================================="

# Leer inputs del usuario
echo ""
echo "Ingresa tus API keys:"
echo ""

read -sp "Snowflake Account: " SNOWFLAKE_ACCOUNT
echo ""
read -sp "Snowflake User: " SNOWFLAKE_USER
echo ""
read -sp "Snowflake Password: " SNOWFLAKE_PASSWORD
echo ""
read -sp "Gemini API Key: " GEMINI_API_KEY
echo ""
read -sp "ElevenLabs API Key: " ELEVENLABS_API_KEY
echo ""

# Generar SSH Key
echo ""
echo "Generando SSH Key para la VM..."
SSH_KEY_PATH="$HOME/.ssh/asesor-pyme-key"
mkdir -p ~/.ssh
ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N "" -C "asesor-pyme-azure"
print_success "SSH Key generada"

# Guardar secrets en archivo temporal
cat > /tmp/gh_secrets.txt << EOF
# Azure Secrets
AZURE_CREDENTIALS=$(echo $SP_OUTPUT | jq -c '.')

# SSH Secret
AZURE_SSH_KEY=$(cat "${SSH_KEY_PATH}")

# API Keys
SNOWFLAKE_ACCOUNT=${SNOWFLAKE_ACCOUNT}
SNOWFLAKE_USER=${SNOWFLAKE_USER}
SNOWFLAKE_PASSWORD=${SNOWFLAKE_PASSWORD}
GEMINI_API_KEY=${GEMINI_API_KEY}
ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
EOF

echo ""
echo "========================================="
echo "3. Instrucciones para GitHub"
echo "========================================="

echo ""
print_success "Secrets generados en /tmp/gh_secrets.txt"
echo ""
echo "Para configurar manualmente en GitHub:"
echo "1. Ve a tu repositorio en GitHub"
echo "2. Settings → Secrets and variables → Actions"
echo "3. New repository secret"
echo "4. Copia y pega cada secret del archivo /tmp/gh_secrets.txt"
echo ""

# Si gh CLI está instalado, intentar configurar automáticamente
if command -v gh &> /dev/null; then
    echo "¿Quieres configurar los secrets automáticamente? (y/n)"
    read -r REPLY
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh auth login
        
        while IFS='=' read -r KEY VALUE; do
            if [[ ! "$KEY" =~ ^# ]] && [[ -n "$VALUE" ]]; then
                echo "Setting secret: $KEY"
                gh secret set "$KEY" -b "$VALUE"
            fi
        done < /tmp/gh_secrets.txt
        
        print_success "Secrets configurados automáticamente"
    fi
fi

echo ""
echo "========================================="
echo "✅ Configuración completada"
echo "========================================="
echo ""
echo "Próximos pasos:"
echo "1. Si configuraste los secrets manualmente, el archivo está en /tmp/gh_secrets.txt"
echo "2. Haz commit y push a main para activar el deployment"
echo "3. Monitorea el deployment en GitHub Actions"
echo ""
echo "Ver detalles en: azure/README.md"
echo ""

# Limpiar archivo temporal (preguntar primero)
echo "¿Quieres eliminar el archivo temporal de secrets? (y/n)"
read -r REPLY
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f /tmp/gh_secrets.txt
    print_success "Archivo temporal eliminado"
else
    print_warning "Archivo temporal guardado en /tmp/gh_secrets.txt (ELIMÍNALO DESPUÉS DE USAR)"
fi

