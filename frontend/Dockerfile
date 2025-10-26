# Dockerfile para Asesor PyME - Frontend
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias (incluyendo devDependencies para build)
RUN npm ci

# Copiar código fuente
COPY . .

# Construir aplicación
RUN npm run build

# Instalar servidor HTTP
RUN npm install -g http-server

# Exponer puerto
EXPOSE 3000

# Comando para servir la aplicación
CMD ["http-server", "build", "-p", "3000", "-a", "0.0.0.0"]
