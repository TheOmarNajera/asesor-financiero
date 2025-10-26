# 🔍 Diagnóstico y URLs para Probar

## IP de la VM: 34.136.226.244

## 🔧 Diagnóstico desde Google Cloud Shell

### 1. Conectarse a la VM desde Cloud Shell

```bash
# En Google Cloud Shell
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a
```

### 2. Una vez conectado, verificar estado de contenedores:

```bash
# Ver contenedores
docker-compose ps

# Ver logs del frontend (últimas 50 líneas)
docker-compose logs --tail=50 frontend

# Ver logs del backend (últimas 50 líneas)
docker-compose logs --tail=50 backend

# Ver logs de nginx (últimas 50 líneas)
docker-compose logs --tail=50 nginx

# Ver todos los logs juntos
docker-compose logs --tail=100
```

### 3. Reiniciar servicios si es necesario:

```bash
# Reiniciar todos
docker-compose restart

# O reiniciar específico
docker-compose restart backend
docker-compose restart frontend
docker-compose restart nginx

# Reconstruir y levantar de nuevo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 4. Verificar que los puertos estén escuchando:

```bash
# Ver puertos en uso
sudo netstat -tulpn | grep LISTEN

# O con ss
sudo ss -tulpn | grep LISTEN
```

### 5. Verificar configuración de Nginx:

```bash
# Ver configuración de nginx
docker-compose exec nginx cat /etc/nginx/nginx.conf

# Verificar que existan los certificados SSL
ls -la ssl/
```

### 6. Verificar firewall de GCP (desde Cloud Shell, NO desde la VM):

```bash
# Ver firewall rules
gcloud compute firewall-rules list

# Ver si existe regla para la VM
gcloud compute firewall-rules list | grep asesor-pyme

# Ver detalles de la regla
gcloud compute firewall-rules describe [NOMBRE_DE_LA_REGLA]
```

### 7. Verificar que los servicios respondan internamente:

```bash
# Desde la VM, probar el backend
curl http://localhost:8000/health

# Probar el frontend
curl http://localhost:3000

# Probar nginx
curl -k https://localhost
```

### 8. Si algo está mal, revisar y corregir:

```bash
# Ver variables de entorno del backend
docker-compose exec backend env | grep -E '(SNOWFLAKE|GEMINI|ELEVENLABS)'

# Ver archivo .env
cat .env

# Recrear archivo .env si es necesario
cd ~/asesor-pyme
# ... (copiar el contenido del .env desde los secrets)
```

### URLs para Probar

**Opción 1: HTTPS (puerto 443)**
```
https://34.136.226.244
```
⚠️ Nota: Usa certificado self-signed, el navegador mostrará un warning. Haz clic en "Advanced" → "Proceed".

**Opción 2: HTTP Directo (puertos expuestos)**
```
Frontend: http://34.136.226.244:3000
Backend API: http://34.136.226.244:8000
Health Check: http://34.136.226.244:8000/health
```

**Opción 3: HTTP en puerto 80**
```
http://34.136.226.244
```
⚠️ Nota: Redirige automáticamente a HTTPS (puerto 443)

---

## 🔧 Si No Funciona

### Verificar Estado de Servicios

Desde Cloud Shell o tu terminal con gcloud CLI:

```bash
# Conectarse a la VM
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a

# Ver estado de contenedores
cd ~/asesor-pyme
docker-compose ps

# Ver logs del frontend
docker-compose logs frontend

# Ver logs del backend
docker-compose logs backend

# Ver logs de nginx
docker-compose logs nginx

# Reiniciar todos los servicios
docker-compose restart
```

### Verificar Firewall en GCP

Los puertos deben estar abiertos en el firewall:
- ✅ Puertos abiertos automáticamente en el workflow: 80, 443, 8000

Verificar en la consola de GCP:
1. Vaya a **VPC network** → **Firewall rules**
2. Verifique que exista una regla para **asesor-pyme-vm**
3. Puertos permitidos: **80, 443, 8000**

---

## 🚨 Troubleshooting Común

### "No se puede acceder al sitio"
- Verificar que los contenedores estén corriendo (`docker-compose ps`)
- Verificar que los puertos estén abiertos en el firewall de GCP
- Esperar ~2 minutos después del deployment para que los servicios se inicien

### "SSL Error" o "NET::ERR_CERT_INVALID"
- Es **normal** con certificados self-signed
- Hacer clic en "Advanced" → "Proceed to 34.136.226.244 (unsafe)"

### "CORS Error"
- Verificar que el backend esté configurado para aceptar requests del frontend
- Verificar que `REACT_APP_API_URL` esté configurado correctamente

### "502 Bad Gateway"
- Backend o frontend no están corriendo
- Verificar logs: `docker-compose logs`

---

## 🌐 Configurar Dominio

Una vez verificado que funciona con la IP:

1. **En tu proveedor de dominio** (donde compraste `poweredbymaya.tech`):
   - Crear registro **A**
   - Host: `@`
   - Valor: `34.136.226.244`
   - TTL: `3600`

2. **Esperar propagación DNS** (15 minutos - 48 horas)

3. **Acceder**: https://poweredbymaya.tech

---

## 📊 Ver Estado Actual

Ejecutar este comando para ver el estado en tiempo real:

```bash
gcloud compute ssh asesor-pyme-vm --zone=us-central1-a \
  --command="cd ~/asesor-pyme && docker-compose ps && docker-compose logs --tail=20"
```

