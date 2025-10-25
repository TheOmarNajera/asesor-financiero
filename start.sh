#!/bin/bash

# Script de inicio rápido para Asesor PyME Inteligente
# Hack Mty 2025 - Reto Banorte

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║              🏦 ASESOR PYME INTELIGENTE 🏦                  ║"
    echo "║                                                              ║"
    echo "║              Hack Mty 2025 - Reto Banorte                    ║"
    echo "║              Powered by Azure Arm Architecture              ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Verificar prerrequisitos
check_prerequisites() {
    print_step "Verificando prerrequisitos..."
    
    # Verificar Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION encontrado"
    else
        print_error "Python 3 no está instalado"
        exit 1
    fi
    
    # Verificar Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_status "Node.js $NODE_VERSION encontrado"
    else
        print_error "Node.js no está instalado"
        exit 1
    fi
    
    # Verificar Docker
    if command -v docker &> /dev/null; then
        print_status "Docker encontrado"
    else
        print_warning "Docker no está instalado (opcional para desarrollo local)"
    fi
    
    # Verificar Azure CLI
    if command -v az &> /dev/null; then
        print_status "Azure CLI encontrado"
    else
        print_warning "Azure CLI no está instalado (requerido para deployment)"
    fi
}

# Configurar entorno
setup_environment() {
    print_step "Configurando entorno..."
    
    # Crear archivo .env si no existe
    if [ ! -f ".env" ]; then
        print_info "Creando archivo .env..."
        cat > .env << EOF
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
AZURE_RESOURCE_GROUP=asesor-pyme-rg
AZURE_VM_NAME=asesor-pyme-vm

# Database Configuration
DATABASE_URL=sqlite:///./asesor_pyme.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
EOF
        print_status "Archivo .env creado"
    else
        print_status "Archivo .env ya existe"
    fi
    
    # Crear directorio de datos
    mkdir -p data
    print_status "Directorio de datos creado"
}

# Instalar dependencias del backend
install_backend_deps() {
    print_step "Instalando dependencias del backend..."
    
    cd backend
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        print_info "Creando entorno virtual de Python..."
        python3 -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Instalar dependencias
    print_info "Instalando dependencias de Python..."
    pip install -r requirements.txt
    
    cd ..
    print_status "Dependencias del backend instaladas"
}

# Instalar dependencias del frontend
install_frontend_deps() {
    print_step "Instalando dependencias del frontend..."
    
    cd frontend
    
    # Instalar dependencias de Node.js
    print_info "Instalando dependencias de Node.js..."
    npm install
    
    cd ..
    print_status "Dependencias del frontend instaladas"
}

# Ejecutar aplicación en modo desarrollo
run_development() {
    print_step "Iniciando aplicación en modo desarrollo..."
    
    print_info "Iniciando backend en puerto 8000..."
    cd backend
    source venv/bin/activate
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    
    # Esperar un momento para que el backend se inicie
    sleep 3
    
    print_info "Iniciando frontend en puerto 3000..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Aplicación iniciada en modo desarrollo"
    print_info "Frontend: http://localhost:3000"
    print_info "Backend API: http://localhost:8000"
    print_info "Documentación API: http://localhost:8000/docs"
    
    # Función para limpiar procesos al salir
    cleanup() {
        print_info "Deteniendo aplicación..."
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
        exit 0
    }
    
    # Capturar Ctrl+C
    trap cleanup SIGINT
    
    print_info "Presiona Ctrl+C para detener la aplicación"
    
    # Esperar indefinidamente
    wait
}

# Ejecutar con Docker
run_docker() {
    print_step "Iniciando aplicación con Docker..."
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        exit 1
    fi
    
    print_info "Construyendo y ejecutando contenedores..."
    docker-compose up --build
    
    print_status "Aplicación ejecutándose con Docker"
}

# Deployment en Azure
deploy_azure() {
    print_step "Desplegando en Azure..."
    
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI no está instalado"
        exit 1
    fi
    
    # Verificar login en Azure
    if ! az account show &> /dev/null; then
        print_warning "No estás logueado en Azure. Ejecutando 'az login'..."
        az login
    fi
    
    print_info "Ejecutando deployment en Azure VM con arquitectura Arm..."
    chmod +x azure/deploy.sh
    ./azure/deploy.sh
    
    print_status "Deployment en Azure completado"
}

# Mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones disponibles:"
    echo "  dev, development    Ejecutar en modo desarrollo local"
    echo "  docker              Ejecutar con Docker"
    echo "  azure               Desplegar en Azure VM"
    echo "  setup               Solo configurar entorno e instalar dependencias"
    echo "  help                Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 dev              # Ejecutar en modo desarrollo"
    echo "  $0 docker           # Ejecutar con Docker"
    echo "  $0 azure            # Desplegar en Azure"
    echo "  $0 setup            # Solo configurar entorno"
}

# Función principal
main() {
    print_banner
    
    case "${1:-dev}" in
        "dev"|"development")
            check_prerequisites
            setup_environment
            install_backend_deps
            install_frontend_deps
            run_development
            ;;
        "docker")
            check_prerequisites
            setup_environment
            run_docker
            ;;
        "azure")
            check_prerequisites
            setup_environment
            deploy_azure
            ;;
        "setup")
            check_prerequisites
            setup_environment
            install_backend_deps
            install_frontend_deps
            print_status "Configuración completada. Usa '$0 dev' para ejecutar la aplicación."
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Opción no válida: $1"
            show_help
            exit 1
            ;;
    esac
}

# Ejecutar función principal
main "$@"
