# 🚀 Guía de Instalación - Asesor PyME Inteligente

## 📋 Prerrequisitos

### **Sistema Operativo**
- **Windows**: Windows 10/11
- **macOS**: macOS 10.15+
- **Linux**: Ubuntu 18.04+ / CentOS 7+

### **Software Requerido**
- **Python**: 3.8 o superior
- **Node.js**: 16.0 o superior
- **npm**: 8.0 o superior
- **Git**: Para clonar el repositorio
- **Docker**: Opcional, para containerización

### **Cuentas y APIs**
- **Google Gemini API**: Para funcionalidad de IA
- **Azure Account**: Para despliegue en la nube (opcional)

---

## 🏠 **Instalación Local**

### **Paso 1: Clonar el Repositorio**
```bash
git clone https://github.com/tu-usuario/asesor-financiero.git
cd asesor-financiero
```

### **Paso 2: Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables (usar tu editor preferido)
nano .env
# o
code .env
```

**Variables requeridas en `.env`:**

Configurar en el archivo `backend/.env`:

```env
# Configuración del Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Empresa por Defecto
DEFAULT_EMPRESA_ID=E001

# Configuración de Datos
USE_SAMPLE_DATA=true
SKIP_EXCEL_LOADING=true

# Snowflake Data Cloud
SNOWFLAKE_ACCOUNT=tu_account.snowflakecomputing.com
SNOWFLAKE_USER=tu_usuario
SNOWFLAKE_PASSWORD=tu_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PYME_FINANCIAL
SNOWFLAKE_SCHEMA=PUBLIC

# Google Gemini API
GEMINI_API_KEY=tu_api_key_de_gemini

# ElevenLabs Voice Synthesis
ELEVENLABS_API_KEY=tu_api_key_de_elevenlabs
```

### **Paso 3: Instalar Dependencias del Backend**
```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### **Paso 4: Instalar Dependencias del Frontend**
```bash
# Navegar al directorio frontend
cd ../frontend

# Instalar dependencias
npm install
```

### **Paso 5: Preparar Datos de Ejemplo**
```bash
# Volver al directorio raíz
cd ..

# Crear directorio de datos
mkdir data

# Los archivos Excel de ejemplo ya están incluidos:
# - finanzas_empresa.xlsx
# - finanzas_personales.xlsx
```

### **Paso 6: Ejecutar la Aplicación**

#### **Opción A: Ejecución Manual**
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

#### **Opción B: Usar Script de Inicio**
```bash
# Ejecutar script de inicio automático
chmod +x start.sh
./start.sh
```

### **Paso 7: Verificar Instalación**
- **Backend**: http://127.0.0.1:8000/docs
- **Frontend**: http://localhost:3000
- **API Health**: http://127.0.0.1:8000/health

---

## 🐳 **Instalación con Docker**

### **Paso 1: Construir Imágenes**
```bash
# Construir todas las imágenes
docker-compose build
```

### **Paso 2: Ejecutar Contenedores**
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### **Paso 3: Verificar Servicios**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Nginx**: http://localhost:80

### **Comandos Docker Útiles**
```bash
# Parar servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ver estado de contenedores
docker-compose ps

# Acceder a contenedor backend
docker-compose exec backend bash

# Acceder a contenedor frontend
docker-compose exec frontend sh
```

---

## ☁️ **Despliegue en Azure**

### **Paso 1: Configurar Azure CLI**
```bash
# Instalar Azure CLI
# Windows: https://aka.ms/installazurecliwindows
# macOS: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login en Azure
az login

# Verificar suscripción
az account show
```

### **Paso 2: Configurar Variables de Azure**
```bash
# Editar configuración de Azure
nano azure/config.sh
```

**Variables en `azure/config.sh`:**
```bash
RESOURCE_GROUP="asesor-pyme-rg"
VM_NAME="asesor-pyme-vm"
LOCATION="eastus"
VM_SIZE="Standard_B1s"  # Arm-based VM
ADMIN_USERNAME="azureuser"
```

### **Paso 3: Ejecutar Despliegue**
```bash
# Hacer ejecutable el script
chmod +x azure/deploy.sh

# Ejecutar despliegue
./azure/deploy.sh
```

### **Paso 4: Configurar Gemini API en Azure**
```bash
# Configurar API key en la VM
chmod +x azure/setup-gemini.sh
./azure/setup-gemini.sh
```

### **Paso 5: Monitorear Despliegue**
```bash
# Monitorear servicios
chmod +x azure/monitor.sh
./azure/monitor.sh
```

---

## 🔧 **Configuración Avanzada**

### **Configuración de Base de Datos**
```python
# Para usar PostgreSQL en lugar de SQLite
DATABASE_URL=postgresql://user:password@localhost:5432/asesor_pyme

# Para usar MySQL
DATABASE_URL=mysql://user:password@localhost:3306/asesor_pyme
```

### **Configuración de SSL/TLS**
```bash
# Generar certificados SSL
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configurar Nginx con SSL
# Editar nginx.conf para incluir certificados
```

### **Configuración de Logs**
```python
# Configurar logging en backend/app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🧪 **Pruebas y Validación**

### **Pruebas del Backend**
```bash
# Ejecutar tests
cd backend
python -m pytest tests/

# Pruebas específicas
python -m pytest tests/test_api.py
python -m pytest tests/test_services.py
```

### **Pruebas del Frontend**
```bash
# Ejecutar tests
cd frontend
npm test

# Tests con coverage
npm run test:coverage
```

### **Pruebas de Integración**
```bash
# Probar endpoints de API
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/analysis/profitability
curl http://127.0.0.1:8000/api/chat/suggestions
```

### **Pruebas de Carga**
```bash
# Instalar herramienta de carga
pip install locust

# Ejecutar pruebas de carga
locust -f tests/load_test.py --host=http://127.0.0.1:8000
```

---

## 🐛 **Solución de Problemas**

### **Problemas Comunes**

#### **Error: "Module not found"**
```bash
# Verificar instalación de dependencias
pip list
npm list

# Reinstalar dependencias
pip install -r requirements.txt
npm install
```

#### **Error: "Port already in use"**
```bash
# Encontrar proceso usando el puerto
# Windows:
netstat -ano | findstr :8000
# macOS/Linux:
lsof -i :8000

# Terminar proceso
# Windows:
taskkill /PID <PID> /F
# macOS/Linux:
kill -9 <PID>
```

#### **Error: "GEMINI_API_KEY not found"**
```bash
# Verificar archivo .env
cat .env

# Verificar variable de entorno
echo $GEMINI_API_KEY

# Reconfigurar API key
python azure/setup-gemini.sh
```

#### **Error: "Database connection failed"**
```bash
# Verificar archivo de base de datos
ls -la asesor_pyme.db

# Recrear base de datos
rm asesor_pyme.db
python -c "from app.services.data_service import DataService; DataService().load_financial_data()"
```

### **Logs y Debugging**

#### **Backend Logs**
```bash
# Ver logs en tiempo real
tail -f backend/app.log

# Logs con más detalle
export DEBUG=True
python -m uvicorn app.main:app --reload --log-level debug
```

#### **Frontend Logs**
```bash
# Ver logs del navegador
# Abrir Developer Tools (F12)
# Ir a Console tab

# Logs de npm
npm start --verbose
```

#### **Docker Logs**
```bash
# Logs de todos los servicios
docker-compose logs

# Logs de servicio específico
docker-compose logs backend
docker-compose logs frontend
```

---

## 📊 **Monitoreo y Mantenimiento**

### **Métricas del Sistema**
```bash
# Usar script de monitoreo
./azure/monitor.sh

# Métricas manuales
# CPU y memoria
top
htop

# Espacio en disco
df -h

# Red
netstat -tulpn
```

### **Backup de Datos**
```bash
# Backup de base de datos
cp asesor_pyme.db backup_$(date +%Y%m%d).db

# Backup de archivos Excel
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/
```

### **Actualizaciones**
```bash
# Actualizar dependencias Python
pip list --outdated
pip install --upgrade package_name

# Actualizar dependencias Node.js
npm outdated
npm update

# Actualizar aplicación
git pull origin main
docker-compose build --no-cache
docker-compose up -d
```

---

## 🆘 **Soporte y Recursos**

### **Documentación Adicional**
- **README.md**: Descripción general del proyecto
- **DEMO.md**: Guía para el video demo
- **API Documentation**: http://127.0.0.1:8000/docs

### **Recursos Externos**
- **Google Gemini API**: https://ai.google.dev/
- **Azure Documentation**: https://docs.microsoft.com/azure/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://reactjs.org/docs/

### **Contacto**
- **Issues**: Crear issue en GitHub
- **Email**: [tu-email@ejemplo.com]
- **Discord**: [canal del hackathon]

---

## ✅ **Checklist de Instalación**

### **Instalación Local**
- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado
- [ ] Repositorio clonado
- [ ] Variables de entorno configuradas
- [ ] Dependencias backend instaladas
- [ ] Dependencias frontend instaladas
- [ ] Backend ejecutándose en puerto 8000
- [ ] Frontend ejecutándose en puerto 3000
- [ ] API respondiendo correctamente
- [ ] Chat funcionando con Gemini

### **Instalación Docker**
- [ ] Docker instalado
- [ ] Docker Compose instalado
- [ ] Imágenes construidas
- [ ] Contenedores ejecutándose
- [ ] Servicios accesibles
- [ ] Logs sin errores

### **Despliegue Azure**
- [ ] Azure CLI configurado
- [ ] VM creada con arquitectura Arm
- [ ] Puertos abiertos (80, 443, 8000)
- [ ] Aplicación desplegada
- [ ] Gemini API configurada
- [ ] Servicios monitoreados

---

**🚀 ¡Instalación completada! El Asesor PyME Inteligente está listo para transformar la gestión financiera empresarial.**