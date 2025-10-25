#!/bin/bash

# Script de deployment para Azure VM con arquitectura Arm
# Asesor PyME Inteligente - Hack Mty 2025

set -e

echo "🚀 Iniciando deployment en Azure VM con arquitectura Arm..."

# Variables de configuración
RESOURCE_GROUP="asesor-pyme-rg"
VM_NAME="asesor-pyme-vm"
LOCATION="eastus"
VM_SIZE="Standard_D2ps_v5"  # VM con procesador Arm
ADMIN_USERNAME="azureuser"
IMAGE="Ubuntu2204"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Azure CLI está instalado
if ! command -v az &> /dev/null; then
    print_error "Azure CLI no está instalado. Por favor instálalo desde: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Verificar login en Azure
if ! az account show &> /dev/null; then
    print_warning "No estás logueado en Azure. Ejecutando 'az login'..."
    az login
fi

print_status "Creando grupo de recursos..."
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

print_status "Creando VM con arquitectura Arm..."
az vm create \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --image $IMAGE \
    --size $VM_SIZE \
    --admin-username $ADMIN_USERNAME \
    --generate-ssh-keys \
    --public-ip-sku Standard \
    --output table

print_status "Abriendo puertos necesarios..."
az vm open-port \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --port 80 \
    --priority 1000

az vm open-port \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --port 443 \
    --priority 1001

az vm open-port \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --port 8000 \
    --priority 1002

print_status "Obteniendo IP pública de la VM..."
VM_IP=$(az vm show \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --show-details \
    --query publicIps \
    --output tsv)

print_status "IP pública de la VM: $VM_IP"

# Crear script de instalación para la VM
cat > install-dependencies.sh << 'EOF'
#!/bin/bash

# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar Git
sudo apt-get install -y git

# Instalar Node.js (para desarrollo)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Python y pip
sudo apt-get install -y python3 python3-pip python3-venv

# Crear directorio para la aplicación
mkdir -p /home/azureuser/asesor-pyme
cd /home/azureuser/asesor-pyme

echo "✅ Dependencias instaladas correctamente"
EOF

print_status "Copiando script de instalación a la VM..."
scp -o StrictHostKeyChecking=no install-dependencies.sh $ADMIN_USERNAME@$VM_IP:/home/$ADMIN_USERNAME/

print_status "Ejecutando instalación de dependencias en la VM..."
ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "chmod +x install-dependencies.sh && ./install-dependencies.sh"

print_status "Copiando código de la aplicación a la VM..."
scp -o StrictHostKeyChecking=no -r . $ADMIN_USERNAME@$VM_IP:/home/$ADMIN_USERNAME/asesor-pyme/

print_status "Configurando variables de entorno en la VM..."
ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && echo 'GEMINI_API_KEY=your_gemini_api_key_here' > .env"

print_status "Construyendo y ejecutando aplicación con Docker Compose..."
ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && docker-compose up -d --build"

print_status "Esperando que los servicios estén listos..."
sleep 30

print_status "Verificando estado de los servicios..."
ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && docker-compose ps"

print_status "✅ Deployment completado exitosamente!"
print_status "🌐 Aplicación disponible en: http://$VM_IP"
print_status "📊 API disponible en: http://$VM_IP/api"
print_status "🔧 Para conectarte a la VM: ssh $ADMIN_USERNAME@$VM_IP"

# Limpiar archivos temporales
rm -f install-dependencies.sh

print_status "🎉 ¡Asesor PyME Inteligente está ejecutándose en Azure con arquitectura Arm!"
print_status "💡 Recuerda configurar tu API key de Google Gemini en el archivo .env"
