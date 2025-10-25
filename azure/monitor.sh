#!/bin/bash

# Script para monitorear la aplicación en Azure VM
# Asesor PyME Inteligente

set -e

# Variables
RESOURCE_GROUP="asesor-pyme-rg"
VM_NAME="asesor-pyme-vm"
ADMIN_USERNAME="azureuser"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Asesor PyME - Monitoreo${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Obtener IP de la VM
get_vm_ip() {
    az vm show \
        --resource-group $RESOURCE_GROUP \
        --name $VM_NAME \
        --show-details \
        --query publicIps \
        --output tsv
}

# Verificar estado de la VM
check_vm_status() {
    print_status "Verificando estado de la VM..."
    VM_STATUS=$(az vm show \
        --resource-group $RESOURCE_GROUP \
        --name $VM_NAME \
        --query "provisioningState" \
        --output tsv)
    
    if [ "$VM_STATUS" = "Succeeded" ]; then
        print_status "✅ VM está ejecutándose correctamente"
    else
        print_error "❌ VM no está funcionando correctamente"
        return 1
    fi
}

# Verificar servicios Docker
check_docker_services() {
    print_status "Verificando servicios Docker..."
    VM_IP=$(get_vm_ip)
    
    ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && docker-compose ps"
}

# Verificar conectividad de la aplicación
check_app_connectivity() {
    print_status "Verificando conectividad de la aplicación..."
    VM_IP=$(get_vm_ip)
    
    # Verificar backend
    if curl -f -s "http://$VM_IP/api/health" > /dev/null; then
        print_status "✅ Backend API está respondiendo"
    else
        print_error "❌ Backend API no está respondiendo"
    fi
    
    # Verificar frontend
    if curl -f -s "http://$VM_IP" > /dev/null; then
        print_status "✅ Frontend está respondiendo"
    else
        print_error "❌ Frontend no está respondiendo"
    fi
}

# Mostrar logs de la aplicación
show_logs() {
    print_status "Mostrando logs de la aplicación..."
    VM_IP=$(get_vm_ip)
    
    ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && docker-compose logs --tail=50"
}

# Reiniciar servicios
restart_services() {
    print_status "Reiniciando servicios..."
    VM_IP=$(get_vm_ip)
    
    ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "cd /home/$ADMIN_USERNAME/asesor-pyme && docker-compose restart"
    
    print_status "Esperando que los servicios se inicien..."
    sleep 30
    
    check_app_connectivity
}

# Mostrar métricas de recursos
show_resource_metrics() {
    print_status "Métricas de recursos de la VM..."
    VM_IP=$(get_vm_ip)
    
    ssh -o StrictHostKeyChecking=no $ADMIN_USERNAME@$VM_IP "free -h && df -h"
}

# Función principal
main() {
    print_header
    
    case "${1:-status}" in
        "status")
            check_vm_status
            check_docker_services
            check_app_connectivity
            ;;
        "logs")
            show_logs
            ;;
        "restart")
            restart_services
            ;;
        "metrics")
            show_resource_metrics
            ;;
        "all")
            check_vm_status
            check_docker_services
            check_app_connectivity
            show_resource_metrics
            ;;
        *)
            echo "Uso: $0 {status|logs|restart|metrics|all}"
            echo ""
            echo "Comandos disponibles:"
            echo "  status  - Verificar estado general (por defecto)"
            echo "  logs    - Mostrar logs de la aplicación"
            echo "  restart - Reiniciar servicios"
            echo "  metrics - Mostrar métricas de recursos"
            echo "  all     - Ejecutar todas las verificaciones"
            exit 1
            ;;
    esac
    
    VM_IP=$(get_vm_ip)
    echo ""
    print_status "🌐 Aplicación disponible en: http://$VM_IP"
    print_status "📊 API disponible en: http://$VM_IP/api"
}

# Ejecutar función principal
main "$@"
