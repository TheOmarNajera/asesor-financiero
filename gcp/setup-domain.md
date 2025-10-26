# 🌐 Configuración de Dominio - poweredbymaya.tech

## 📋 Pasos para Configurar el Dominio en GCP

### 1. Obtener IP de la VM

Primero, obtén la IP pública de tu VM en GCP:

```bash
gcloud compute instances describe asesor-pyme-vm \
  --zone=us-central1-a \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

O desde la consola de GCP:
1. Ve a **Compute Engine** → **VM instances**
2. Busca **asesor-pyme-vm**
3. Copia la **IP externa**

### 2. Configurar DNS Records

En tu proveedor de dominio (donde compraste `poweredbymaya.tech`):

#### Crear un Record Tipo A
```
Tipo: A
Host/Name: @
Valor/Content: [IP de la VM de GCP]
TTL: 3600
```

#### (Opcional) Subdominio www
```
Tipo: A
Host/Name: www
Valor/Content: [IP de la VM de GCP]
TTL: 3600
```

### 3. Configurar Certificado SSL

El deployment automático ya crea certificados self-signed para testing inicial.

Para usar certificados Let's Encrypt (producción):

```bash
# Conectarse a la VM
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a

# Instalar Certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d poweredbymaya.tech -d www.poweredbymaya.tech

# Configurar renovación automática
sudo certbot renew --dry-run
```

### 4. Actualizar CORS en Backend

Ya está configurado en `backend/app/main.py` para permitir tu dominio.

Si necesitas agregarlo manualmente:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://poweredbymaya.tech",
        "https://www.poweredbymaya.tech",
        "http://[TU_IP_GCP]:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Verificar Configuración

Después de configurar DNS (puede tomar hasta 48 horas propagarse):

```bash
# Verificar DNS
nslookup poweredbymaya.tech

# Verificar HTTPS
curl -I https://poweredbymaya.tech

# Verificar Health Check
curl https://poweredbymaya.tech/health
```

## 🚀 URLs para Probar ANTES de Configurar Dominio

### Obtener IP de la VM

```bash
gcloud compute instances describe asesor-pyme-vm \
  --zone=us-central1-a \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### URLs de Acceso Directo

Una vez tengas la IP (ejemplo: `34.136.226.244`):

- **Frontend (HTTP)**: http://34.136.226.244:3000
- **Frontend (HTTPS)**: https://34.136.226.244
- **API**: https://34.136.226.244/api
- **Health Check**: https://34.136.226.244/health

**Nota**: Los certificados self-signed mostrarán un warning de seguridad. Es normal para testing.

## 🔧 Comandos Útiles

### Conectarse a la VM
```bash
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a
```

### Ver Logs de Docker
```bash
# Desde la VM
cd ~/asesor-pyme
docker-compose logs -f

# Ver solo logs del backend
docker-compose logs -f backend

# Ver solo logs del frontend
docker-compose logs -f frontend
```

### Reiniciar Servicios
```bash
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a \
  --command="cd ~/asesor-pyme && docker-compose restart"
```

### Verificar Estado de Servicios
```bash
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a \
  --command="cd ~/asesor-pyme && docker-compose ps"
```

## 📊 Verificar que Funciona

### Verificar DNS (después de configurar)
1. **DNS Propagado**: https://dnschecker.org/#A/poweredbymaya.tech
2. **SSL Funcionando**: https://www.ssllabs.com/ssltest/analyze.html?d=poweredbymaya.tech
3. **Aplicación**: https://poweredbymaya.tech

## ⚠️ Troubleshooting

### Dominio no responde
- Verificar que los DNS records estén configurados correctamente
- Esperar propagación DNS (hasta 48 horas)
- Verificar que la VM tenga IP pública
- Verificar firewall rules en GCP

### SSL no funciona
- Verificar que el puerto 443 esté abierto en GCP
- Verificar que los certificados estén instalados
- Revisar logs de Nginx
- Los certificados self-signed mostrarán warnings (normal)

### CORS errors
- Actualizar `allow_origins` en el backend
- Verificar headers en las requests
- Asegurar que el dominio esté en la lista de permitidos

## 🎯 Checklist de Dominio

- [ ] Obtener IP de la VM en GCP
- [ ] DNS records configurados (A record) en tu proveedor
- [ ] DNS propagado (verificar en dnschecker.org)
- [ ] Certificados SSL instalados (self-signed para testing o Let's Encrypt para prod)
- [ ] Nginx configurado con el dominio
- [ ] CORS actualizado en el backend
- [ ] HTTPS funcionando
- [ ] Frontend accesible en https://poweredbymaya.tech

---

**🌐 ¡Tu aplicación estará disponible en https://poweredbymaya.tech!**

**🚀 Para probar ahora: usa la IP de GCP directamente**

