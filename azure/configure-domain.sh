#!/bin/bash

# Script para configurar dominio y SSL en la VM
# Asesor PyME Inteligente

set -e

DOMAIN_NAME="${1:-poweredbymaya.tech}"
EMAIL="${2:-admin@poweredbymaya.tech}"

echo "🌐 Configurando dominio: $DOMAIN_NAME"
echo "📧 Email para certificados: $EMAIL"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Actualizar sistema
print_success "Actualizando sistema..."
sudo apt-get update -y

# Instalar Certbot
if ! command -v certbot &> /dev/null; then
    print_success "Instalando Certbot..."
    sudo apt-get install -y certbot python3-certbot-nginx
fi

# Detener Nginx temporalmente para obtener certificado
print_success "Deteniendo Nginx temporalmente..."
sudo docker-compose down nginx 2>/dev/null || true

# Obtener certificado
print_success "Obteniendo certificado SSL..."
sudo certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN_NAME" \
    -d "www.$DOMAIN_NAME"

# Configurar renovación automática
print_success "Configurando renovación automática..."
sudo systemctl enable certbot.timer

# Reiniciar servicios
print_success "Reiniciando servicios..."
sudo docker-compose up -d

print_success "✅ Dominio configurado exitosamente!"
echo ""
echo "🌐 Tu aplicación está disponible en:"
echo "   - https://$DOMAIN_NAME"
echo "   - https://www.$DOMAIN_NAME"
echo ""
echo "📋 Para verificar:"
echo "   curl -I https://$DOMAIN_NAME"

