#!/bin/bash

# Script para verificar el deployment en la VM de GCP

VM_IP="34.136.226.244"
VM_ZONE="us-central1-a"
VM_NAME="asesor-pyme-vm"

echo "🔍 Verificando deployment en la VM $VM_NAME..."

# Conectarse y verificar estado de Docker
echo "📊 Estado de Docker Compose:"
gcloud compute ssh asesor-pyme-vm \
  --zone=$VM_ZONE \
  --command="cd ~/asesor-pyme && docker-compose ps"

echo ""
echo "📝 Últimos logs del backend:"
gcloud compute ssh asesor-pyme-vm \
  --zone=$VM_ZONE \
  --command="cd ~/asesor-pyme && docker-compose logs --tail=50 backend"

echo ""
echo "📝 Últimos logs del frontend:"
gcloud compute ssh asesor-pyme-vm \
  --zone=$VM_ZONE \
  --command="cd ~/asesor-pyme && docker-compose logs --tail=50 frontend"

echo ""
echo "📝 Últimos logs de nginx:"
gcloud compute ssh asesor-pyme-vm \
  --zone=$VM_ZONE \
  --command="cd ~/asesor-pyme && docker-compose logs --tail=50 nginx"

echo ""
echo "🌐 URLs para probar:"
echo "  - http://$VM_IP:3000 (Frontend)"
echo "  - http://$VM_IP:8000 (Backend API)"
echo "  - http://$VM_IP:8000/health (Health Check)"
echo "  - https://$VM_IP (HTTPS)"

echo ""
echo "🔧 Si hay errores, intentar reiniciar:"
echo "  gcloud compute ssh asesor-pyme-vm --zone=$VM_ZONE --command='cd ~/asesor-pyme && docker-compose restart'"

