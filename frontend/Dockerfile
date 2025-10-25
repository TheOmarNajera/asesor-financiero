# Dockerfile para Asesor PyME - Frontend
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY frontend/package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY frontend/ .

# Construir aplicación
RUN npm run build

# Instalar servidor estático
RUN npm install -g serve

# Exponer puerto
EXPOSE 3000

# Comando para servir la aplicación
CMD ["serve", "-s", "build", "-l", "3000"]
