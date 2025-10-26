# 🚀 Instrucciones de Deployment - Asesor PyME Inteligente

## 🎯 Resumen Rápido

Este proyecto tiene **deployment automático** a Azure VM con arquitectura Arm cada vez que haces push a `main`.

## ⚡ Setup Inicial (Una vez)

### Paso 1: Configurar GitHub Secrets

Ejecuta el script de setup:

```bash
chmod +x azure/setup-github-secrets.sh
./azure/setup-github-secrets.sh
```

O configura manualmente en GitHub:
1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Agrega los siguientes secrets:

#### Azure Secrets
- `AZURE_CREDENTIALS` - JSON del Service Principal
- `AZURE_SSH_KEY` - Clave privada SSH

#### API Keys
- `SNOWFLAKE_ACCOUNT` - Tu cuenta de Snowflake
- `SNOWFLAKE_USER` - Usuario de Snowflake
- `SNOWFLAKE_PASSWORD` - Password de Snowflake
- `GEMINI_API_KEY` - Tu API key de Google Gemini
- `ELEVENLABS_API_KEY` - Tu API key de ElevenLabs

### Paso 2: Crear Resource Group

```bash
az login
az group create --name asesor-pyme-rg --location eastus
```

## 🚀 Deployment Automático

Una vez configurado, cada push a `main` desplegará automáticamente:

```bash
git add .
git commit -m "Update application"
git push origin main
```

El workflow de GitHub Actions:
1. ✅ Crea la VM si no existe (Arm architecture)
2. ✅ Instala Docker y dependencias
3. ✅ Clona tu código
4. ✅ Configura variables de entorno
5. ✅ Build y deploy con Docker Compose
6. ✅ Health check

## 📊 Verificar Deployment

### Obtener IP de la VM
```bash
az vm show \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm \
  --show-details \
  --query publicIps \
  --output tsv
```

### Health Check
```bash
curl http://TU_VM_IP/health
```

### Ver logs
Ve a **GitHub** → **Actions** para ver el progreso del deployment.

## 🔧 Configuración Local (Opcional)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📚 Documentación Adicional

- [Guía completa de deployment](../azure/README.md)
- [Configuración de variables de entorno](../env.example)
- [API Endpoints](../README.md)

## 💰 Costos Estimados

- **VM Arm (Standard_D2ps_v5)**: ~$50/month
- **Storage**: ~$10/month
- **Total**: ~$60/month

## 🆘 Troubleshooting

### El deployment falla
1. Ve a GitHub Actions y revisa los logs
2. Verifica que los GitHub Secrets estén configurados
3. Verifica que el Service Principal tenga permisos

### La VM no responde
```bash
az vm restart --resource-group asesor-pyme-rg --name asesor-pyme-vm
```

### Ver logs en la VM
```bash
ssh azureuser@TU_VM_IP
cd ~/asesor-pyme
docker-compose logs -f
```

## ✅ Checklist Pre-Deployment

- [ ] GitHub Secrets configurados
- [ ] Resource Group creado en Azure
- [ ] Pruebas locales pasando
- [ ] Código listo para producción
- [ ] API keys válidas
- [ ] .gitignore actualizado
- [ ] DNS configurado (A record → IP de VM)
- [ ] Certificado SSL configurado

## 🌐 Configuración de Dominio poweredbymaya.tech

### 1. Configurar DNS
En tu proveedor de dominio, crear:
```
Tipo: A
Host: @
Valor: [IP DE TU VM]
TTL: 3600
```

### 2. Obtener IP de VM
```bash
az vm show \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm \
  --show-details \
  --query publicIps \
  --output tsv
```

### 3. Configurar SSL (después del deployment)
```bash
# Conectarse a la VM
ssh azureuser@[TU_VM_IP]

# Ejecutar script de configuración
cd ~/asesor-pyme
chmod +x azure/configure-domain.sh
sudo ./azure/configure-domain.sh poweredbymaya.tech
```

**Ver [azure/setup-domain.md](azure/setup-domain.md) para instrucciones detalladas.**

## 🎉 Una vez completado

Tu aplicación estará disponible en:
- **Frontend**: https://poweredbymaya.tech
- **API**: https://poweredbymaya.tech/api
- **Health**: https://poweredbymaya.tech/health

---

**🚀 ¡Deployment automático configurado con Azure Arm!**

