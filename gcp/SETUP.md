# 🚀 Guía de Setup para GCP (Google Cloud Platform)

## 📋 Prerrequisitos

1. **Cuenta de Google Cloud** (trial gratuito incluye $300 de créditos)
2. **Repositorio en GitHub** configurado
3. **GitHub Secrets** configurados

## 🔧 Configuración Inicial

### 1. Crear Proyecto en GCP

```bash
# Instalar Google Cloud SDK
# Windows: https://cloud.google.com/sdk/docs/install-sdk#windows
# macOS: brew install --cask google-cloud-sdk
# Linux: https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Crear proyecto
gcloud projects create asesor-pyme-2025 --name="Asesor PyME"

# Configurar proyecto
gcloud config set project asesor-pyme-2025
```

### 2. Crear Service Account

```bash
# Crear service account
gcloud iam service-accounts create github-actions --display-name="GitHub Actions Service Account"

# Otorgar permisos
gcloud projects add-iam-policy-binding asesor-pyme-2025 \
  --member="serviceAccount:github-actions@asesor-pyme-2025.iam.gserviceaccount.com" \
  --role="roles/compute.instanceAdmin.v1"

gcloud projects add-iam-policy-binding asesor-pyme-2025 \
  --member="serviceAccount:github-actions@asesor-pyme-2025.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding asesor-pyme-2025 \
  --member="serviceAccount:github-actions@asesor-pyme-2025.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageAdmin"

# Crear clave JSON
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@asesor-pyme-2025.iam.gserviceaccount.com

# Leer clave JSON desde cloud shell
cat key.json
```

### 3. Habilitar APIs Necesarias

```bash
gcloud services enable compute.googleapis.com
gcloud services enable iam.googleapis.com
```

### 4. Configurar GitHub Secrets

En tu repositorio de GitHub:

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Agrega estos secrets:

#### GCP Secrets
- `GCP_PROJECT_ID`: `asesor-pyme-2025` (o tu project ID)
- `GCP_SA_KEY`: Contenido completo del archivo `key.json` que creaste
- `AZURE_CREDENTIALS`: (ya no necesario)
- `AZURE_SSH_KEY`: (ya no necesario)

#### API Keys (mantener)
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `GEMINI_API_KEY`
- `ELEVENLABS_API_KEY`

## 🚀 Deployment

### Automático (Recomendado)

Una vez configurados los secrets:

```bash
git add .
git commit -m "Configure GCP deployment"
git push origin main
```

El workflow se ejecutará automáticamente.

### Manual

Si necesitas crear la VM manualmente:

```bash
# Crear VM con ARM
gcloud compute instances create asesor-pyme-vm \
  --zone=europe-west1-c \
  --machine-type=t2a-standard-2 \
  --image-family=ubuntu-2204-lts-arm64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard \
  --tags=http-server,https-server

# Abrir puertos
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server

gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --source-ranges 0.0.0.0/0 \
  --target-tags https-server

gcloud compute firewall-rules create allow-8000 \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server
```

## 🌐 Configurar Dominio

Una vez tengas la IP de la VM:

```bash
# Obtener IP
gcloud compute instances describe asesor-pyme-vm \
  --zone=europe-west1-c \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

1. En tu proveedor de dominio, crear A record:
   - Host: `@`
   - Valor: [IP de la VM]
   - TTL: 3600

2. Después del primer deployment, configurar SSL:
```bash
# Conectarse a la VM
gcloud compute ssh asesor-pyme-vm --zone=europe-west1-c

# Configurar SSL
cd ~/asesor-pyme
chmod +x gcp/configure-domain.sh
sudo ./gcp/configure-domain.sh poweredbymaya.tech
```

## 💰 Costos Estimados

- **VM (t2a-standard-2)**: ~$60/month
- **Network**: Gratis en tier básico
- **Storage (20GB)**: ~$3/month
- **Total**: ~$63/month

Los primeros $300 son gratis (trial).

## 🔍 Verificar Deployment

```bash
# Obtener IP de la VM
VM_IP=$(gcloud compute instances describe asesor-pyme-vm \
  --zone=europe-west1-c \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)")

# Health check
curl -k https://$VM_IP/health

# Ver logs
gcloud compute ssh asesor-pyme-vm --zone=europe-west1-c \
  --command="cd ~/asesor-pyme && docker compose logs -f"
```

## 🛠️ Troubleshooting

### VM no responde
```bash
# Ver estado de la VM
gcloud compute instances describe asesor-pyme-vm \
  --zone=europe-west1-c \
  --format="value(status)"

# Reiniciar
gcloud compute instances reset asesor-pyme-vm --zone=europe-west1-c
```

### Ver logs de deployment
GitHub → Actions → Selecciona el workflow fallido

### Limpiar recursos
```bash
# Eliminar VM
gcloud compute instances delete asesor-pyme-vm --zone=europe-west1-c

# Eliminar firewall rules
gcloud compute firewall-rules delete allow-http allow-https allow-8000
```

## ✅ Checklist

- [ ] GCP Project creado
- [ ] Service Account creado y configurado
- [ ] `key.json` descargado y agregado a GitHub Secrets
- [ ] APIs habilitadas (Compute, IAM)
- [ ] GitHub Secrets configurados
- [ ] Dominio DNS configurado
- [ ] Push a main activado

---

**🚀 ¡Listo para deployment en GCP con arquitectura Arm!**

