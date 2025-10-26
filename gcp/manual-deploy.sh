#!/bin/bash
# Script para clonar y deployar manualmente en la VM

set -e

echo "🚀 Iniciando deployment manual..."

# Clonar repositorio
cd ~
if [ ! -d "asesor-pyme" ]; then
    echo "📦 Clonando repositorio..."
    git clone https://github.com/eonajera-deacero/asesor-financiero.git asesor-pyme
    cd asesor-pyme
else
    echo "📦 Actualizando repositorio existente..."
    cd asesor-pyme
    git pull
fi

# Crear .env
echo "⚙️ Creando archivo .env..."
cat > .env << 'EOF'
HOST=0.0.0.0
PORT=8000
DEBUG=False
DEFAULT_EMPRESA_ID=E001
USE_SAMPLE_DATA=true
SKIP_EXCEL_LOADING=true
EOF

# Nota: Las keys de Snowflake, Gemini y ElevenLabs deben agregarse manualmente
# o desde GitHub Secrets

# Crear certificados SSL
echo "🔒 Creando certificados SSL..."
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem \
  -subj "/CN=localhost"

# Crear directorio data si no existe
mkdir -p data

# Verificar docker-compose
echo "🐳 Verificando Docker..."
docker --version
docker-compose --version

# Levantar servicios
echo "🚀 Levantando servicios..."
docker-compose down
docker-compose build
docker-compose up -d

# Esperar a que inicien
echo "⏳ Esperando que los servicios inicien..."
sleep 30

# Verificar estado
echo "✅ Verificando estado de servicios..."
docker-compose ps

echo "🎉 Deployment completado!"
echo ""
echo "📊 URLs para probar:"
echo "  - https://$(curl -s ifconfig.me)"
echo "  - http://$(curl -s ifconfig.me):3000"
echo "  - http://$(curl -s ifconfig.me):8000"
echo ""
echo "Ver logs: docker-compose logs -f"

