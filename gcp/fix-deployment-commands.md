# 🔧 Comandos para Diagnóstico y Fix

## 1. Ver logs del backend
```bash
docker-compose logs backend
```

## 2. Ver logs del nginx
```bash
docker-compose logs nginx
```

## 3. Ver el error exacto del backend (últimas 100 líneas)
```bash
docker-compose logs --tail=100 backend
```

## 4. Verificar que existe el archivo .env
```bash
cat .env
```

## 5. Verificar que existen los certificados SSL
```bash
ls -la ssl/
```

## 6. Si falta .env, crearlo:
```bash
cat > .env << 'EOF'
HOST=0.0.0.0
PORT=8000
DEBUG=False
DEFAULT_EMPRESA_ID=E001
USE_SAMPLE_DATA=true
SKIP_EXCEL_LOADING=true
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=PYME_FINANCIAL
SNOWFLAKE_SCHEMA=PUBLIC
GEMINI_API_KEY=
ELEVENLABS_API_KEY=
EOF
```

## 7. Si faltan certificados SSL:
```bash
mkdir -p ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem \
  -subj "/CN=localhost"
```

## 8. Reiniciar servicios
```bash
docker-compose down
docker-compose up -d
```

## 9. Ver logs en tiempo real
```bash
docker-compose logs -f
```

## 10. Verificar puertos abiertos
```bash
sudo netstat -tulpn | grep -E ':(80|443|3000|8000)' 
```

## 11. Si todo falla, reconstruir imágenes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

