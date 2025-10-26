# 🚀 Guía de Deployment en Azure VM (Arm)

Esta guía explica cómo configurar el deployment automático del Asesor PyME Inteligente en una VM de Azure con arquitectura Arm.

## 📋 Prerrequisitos

1. **Cuenta de Azure** con suscripción activa
2. **Azure CLI** instalado
3. **Repositorio en GitHub** configurado
4. **GitHub Secrets** configurados (ver abajo)

## 🔧 Configuración de GitHub Secrets

Para que el deployment automático funcione, necesitas configurar estos secrets en GitHub:

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions → New repository secret
3. Agrega los siguientes secrets:

### Azure Secrets
- `AZURE_CREDENTIALS` - Credenciales de Azure (JSON)
  ```bash
  az ad sp create-for-rbac --name "asesor-pyme-github-actions" \
    --role contributor \
    --scopes /subscriptions/YOUR_SUBSCRIPTION_ID \
    --sdk-auth
  ```
  Copia el output JSON completo

- `AZURE_SSH_KEY` - Clave SSH pública
  ```bash
  ssh-keygen -t rsa -b 4096 -C "github-actions@asesor-pyme"
  cat ~/.ssh/id_rsa
  ```
  Copia la clave PRIVADA completa

### API Keys Secrets
- `SNOWFLAKE_ACCOUNT` - Tu cuenta de Snowflake
- `SNOWFLAKE_USER` - Usuario de Snowflake
- `SNOWFLAKE_PASSWORD` - Password de Snowflake
- `GEMINI_API_KEY` - Tu API key de Google Gemini
- `ELEVENLABS_API_KEY` - Tu API key de ElevenLabs

## 🚀 Deployment Automático

### Configuración Inicial

1. **Crear el grupo de recursos en Azure:**
```bash
az group create \
  --name asesor-pyme-rg \
  --location eastus
```

2. **El deployment automático se activará:**
   - Cada push a la rama `main`
   - Manualmente desde GitHub Actions

### Proceso de Deployment

El workflow de GitHub Actions realizará automáticamente:

1. ✅ Verificar que Azure CLI está instalado
2. ✅ Login en Azure
3. ✅ Crear Resource Group si no existe
4. ✅ Crear VM con arquitectura Arm (`Standard_D2ps_v5`) si no existe
5. ✅ Abrir puertos 80, 443, 8000
6. ✅ Instalar Docker y Docker Compose en la VM
7. ✅ Clonar/pull del código desde GitHub
8. ✅ Crear archivo `.env` con las variables de entorno
9. ✅ Build y deploy con Docker Compose
10. ✅ Health check

## 🌐 Acceso a la Aplicación

Una vez completado el deployment:

- **Frontend**: http://TU_VM_IP
- **Backend API**: http://TU_VM_IP/api
- **Health Check**: http://TU_VM_IP/health

### Obtener la IP de la VM

```bash
az vm show \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm \
  --show-details \
  --query publicIps \
  --output tsv
```

## 🔄 Actualización Manual

Si necesitas actualizar manualmente:

```bash
# Conectarse a la VM
ssh azureuser@TU_VM_IP

# Ir al directorio de la app
cd ~/asesor-pyme

# Pull de los últimos cambios
git pull

# Rebuild y restart
docker-compose down
docker-compose build
docker-compose up -d
```

## 📊 Monitoreo

### Ver logs de los servicios

```bash
ssh azureuser@TU_VM_IP
cd ~/asesor-pyme
docker-compose logs -f
```

### Verificar estado de los servicios

```bash
docker-compose ps
```

### Health Check

```bash
curl http://TU_VM_IP/health
```

## 🛠️ Troubleshooting

### VM no responde

```bash
# Verificar el estado de la VM
az vm show \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm \
  --show-details

# Reiniciar la VM
az vm restart \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm
```

### Revisar logs del workflow

1. Ve a GitHub → Actions
2. Selecciona el workflow fallido
3. Revisa los logs de cada step

### Limpiar recursos

```bash
# Eliminar todo el resource group
az group delete --name asesor-pyme-rg --yes
```

## 💰 Costos

- **VM (Standard_D2ps_v5)**: ~$0.07/hour (~$50/month)
- **Storage**: ~$10/month
- **Network**: Gratis en Azure tier
- **Total estimado**: ~$60/month

## 🏆 Arquitectura Arm

La VM usa arquitectura Arm para:
- ✅ Mejor eficiencia energética (MLH Arm prize)
- ✅ Menores costos
- ✅ Mejor rendimiento en cargas de trabajo modernas

## 📚 Documentación Adicional

- [Guía de Docker Compose](docker-compose.yml)
- [Configuración de Nginx](nginx.conf)
- [Variables de Entorno](../env.example)

---

**¡El Asesor PyME Inteligente está listo para deployment automático en Azure!** 🚀

