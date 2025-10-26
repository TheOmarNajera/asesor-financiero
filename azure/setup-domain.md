# 🌐 Configuración de Dominio - poweredbymaya.tech

## 📋 Pasos para Configurar el Dominio

### 1. Configurar DNS Records

En tu proveedor de dominio (donde compraste `poweredbymaya.tech`):

#### Crear un Record Tipo A
```
Tipo: A
Host/Name: @
Valor/Content: [IP DE TU VM DE AZURE]
TTL: 3600
```

#### (Opcional) Subdominio www
```
Tipo: A
Host/Name: www
Valor/Content: [IP DE TU VM DE AZURE]
TTL: 3600
```

**Para obtener la IP de tu VM:**
```bash
az vm show \
  --resource-group asesor-pyme-rg \
  --name asesor-pyme-vm \
  --show-details \
  --query publicIps \
  --output tsv
```

### 2. Configurar Certificado SSL

El deployment automático incluye soporte para Let's Encrypt (certificados SSL gratuitos).

#### Opción A: Certificados SSL con Certbot (Recomendado)

En la VM, ejecutar después del deployment:

```bash
ssh azureuser@[TU_VM_IP]

# Instalar Certbot
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d poweredbymaya.tech -d www.poweredbymaya.tech

# Configurar renovación automática
sudo certbot renew --dry-run
```

#### Opción B: Certificados Self-Signed (Solo para testing)

Ya están incluidos en el deployment para testing inicial.

### 3. Actualizar Nginx Configuration

El archivo `nginx.conf` ya está configurado para:
- Redirigir HTTP → HTTPS
- Usar certificados SSL
- Proxy a backend y frontend

### 4. Actualizar Docker Compose (Opcional)

Si quieres que Nginx escuche específicamente en tu dominio, actualiza:

```yaml
nginx:
  ports:
    - "80:80"
    - "443:443"
  # ... resto de configuración
```

### 5. Configurar CORS en Backend

Actualizar `backend/app/main.py` para permitir tu dominio:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://poweredbymaya.tech",
        "https://www.poweredbymaya.tech"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. Verificar Configuración

Después de configurar DNS (puede tomar hasta 48 horas propagarse):

```bash
# Verificar DNS
nslookup poweredbymaya.tech

# Verificar HTTPS
curl -I https://poweredbymaya.tech

# Verificar Health Check
curl https://poweredbymaya.tech/health
```

## 🚀 Workflow Automático con Dominio

Para automatizar la configuración del certificado SSL:

1. **Actualizar el workflow de GitHub Actions** (ya está preparado)
2. **Agregar secret en GitHub**: `DOMAIN_NAME=poweredbymaya.tech`
3. **El deployment automáticamente**:
   - Configurará Nginx con el dominio
   - Obtendrá certificados SSL con Let's Encrypt
   - Configurará renovación automática

## 🔧 Comandos Útiles

### Renovar Certificado
```bash
sudo certbot renew
```

### Verificar Certificados
```bash
sudo certbot certificates
```

### Ver Logs de Nginx
```bash
sudo tail -f /var/log/nginx/error.log
```

## 📊 Verificar que Funciona

1. **DNS Propagado**: https://dnschecker.org/#A/poweredbymaya.tech
2. **SSL Funcionando**: https://www.ssllabs.com/ssltest/analyze.html?d=poweredbymaya.tech
3. **Aplicación**: https://poweredbymaya.tech

## ⚠️ Troubleshooting

### Dominio no responde
- Verificar que los DNS records estén configurados correctamente
- Esperar propagación DNS (hasta 48 horas)
- Verificar que la VM tenga IP pública

### SSL no funciona
- Verificar que el puerto 443 esté abierto
- Verificar que los certificados estén instalados
- Revisar logs de Nginx

### CORS errors
- Actualizar `allow_origins` en el backend
- Verificar headers en las requests

## 🎯 Checklist de Dominio

- [ ] DNS records configurados (A record)
- [ ] Certificado SSL instalado (Let's Encrypt o self-signed)
- [ ] Nginx configurado con el dominio
- [ ] CORS actualizado en el backend
- [ ] DNS propagado (verificar en dnschecker.org)
- [ ] HTTPS funcionando
- [ ] Frontend accesible en https://poweredbymaya.tech

---

**🌐 ¡Tu aplicación estará disponible en https://poweredbymaya.tech!**

