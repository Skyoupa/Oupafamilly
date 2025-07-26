#!/bin/bash
# Script d'optimisation pour déployement OVH
# Assure la compatibilité avec hébergeurs standards

echo "🌐 OPTIMISATION POUR DÉPLOYEMENT OVH..."

# 1. Vérifier la structure des variables d'environnement
echo "📋 Vérification variables d'environnement..."

# Backend .env
cat > /app/backend/.env.example << EOF
# Variables d'environnement pour déployement OVH
MONGO_URL=mongodb://localhost:27017/oupafamilly
DB_NAME=oupafamilly
JWT_SECRET=your-super-secret-jwt-key-here
PORT=8001

# Variables pour production OVH
# MONGO_URL=mongodb://your-mongo-host:27017/oupafamilly
# DB_NAME=oupafamilly_prod
# JWT_SECRET=production-jwt-secret
# PORT=8001
EOF

# Frontend .env
cat > /app/frontend/.env.example << EOF
# Variables d'environnement frontend pour OVH
REACT_APP_BACKEND_URL=http://localhost:8001

# Variables pour production OVH
# REACT_APP_BACKEND_URL=https://your-domain.com/api
EOF

# 2. Créer un fichier de configuration Docker pour facilité déployement
cat > /app/docker-compose.yml << EOF
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    container_name: oupafamilly_mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: oupafamilly

  backend:
    build: ./backend
    container_name: oupafamilly_backend
    restart: unless-stopped
    ports:
      - "8001:8001"
    depends_on:
      - mongodb
    environment:
      - MONGO_URL=mongodb://mongodb:27017/oupafamilly
      - DB_NAME=oupafamilly
      - JWT_SECRET=your-jwt-secret-here
      - PORT=8001

  frontend:
    build: ./frontend
    container_name: oupafamilly_frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001

volumes:
  mongodb_data:
EOF

# 3. Créer Dockerfile pour backend
cat > /app/backend/Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["python", "server.py"]
EOF

# 4. Créer Dockerfile pour frontend
cat > /app/frontend/Dockerfile << EOF
FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN yarn build

# Serve the application
RUN yarn global add serve
EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
EOF

# 5. Créer script de démarrage pour OVH
cat > /app/start_ovh.sh << EOF
#!/bin/bash
# Script de démarrage pour hébergement OVH

echo "🚀 Démarrage Oupafamilly sur OVH..."

# Installer les dépendances Python backend
echo "📦 Installation dépendances backend..."
cd /app/backend
pip install -r requirements.txt

# Installer les dépendances Node.js frontend
echo "📦 Installation dépendances frontend..."
cd /app/frontend
yarn install

# Build de production frontend
echo "🏗️  Build production frontend..."
yarn build

# Démarrer MongoDB (si pas déjà démarré)
echo "🗄️  Vérification MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "Démarrage MongoDB..."
    mongod --fork --logpath /var/log/mongodb.log
fi

# Démarrer le backend
echo "🔧 Démarrage backend..."
cd /app/backend
python server.py &

# Démarrer le frontend (serveur de production)
echo "🎨 Démarrage frontend..."
cd /app/frontend
serve -s build -l 3000 &

echo "✅ Oupafamilly démarré avec succès!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8001"
EOF

chmod +x /app/start_ovh.sh

# 6. Créer configuration nginx pour OVH
cat > /app/nginx.conf << EOF
server {
    listen 80;
    server_name your-domain.com;

    # Frontend (React)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Servir les fichiers statiques
    location /static {
        alias /app/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 7. Créer documentation de déployement
cat > /app/DEPLOYMENT_OVH.md << EOF
# Déployement Oupafamilly sur OVH

## Prérequis
- Serveur VPS/dédié OVH avec Ubuntu/Debian
- Node.js 16+
- Python 3.9+
- MongoDB 4.4+
- Nginx (optionnel)

## Installation Rapide

### 1. Cloner le projet
\`\`\`bash
git clone <your-repo-url>
cd oupafamilly
\`\`\`

### 2. Configuration
\`\`\`bash
# Copier les fichiers d'exemple
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Modifier les variables selon votre environnement
nano backend/.env
nano frontend/.env
\`\`\`

### 3. Démarrage automatique
\`\`\`bash
chmod +x start_ovh.sh
./start_ovh.sh
\`\`\`

### 4. Avec Docker (recommandé)
\`\`\`bash
docker-compose up -d
\`\`\`

## Configuration Production

### Variables d'environnement
- \`MONGO_URL\`: URL MongoDB (ex: mongodb://localhost:27017/oupafamilly)
- \`REACT_APP_BACKEND_URL\`: URL backend (ex: https://yourdomain.com/api)
- \`JWT_SECRET\`: Clé secrète JWT (générer une clé forte)

### Nginx (optionnel)
\`\`\`bash
sudo cp nginx.conf /etc/nginx/sites-available/oupafamilly
sudo ln -s /etc/nginx/sites-available/oupafamilly /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
\`\`\`

## Maintenance

### Backup base de données
\`\`\`bash
mongodump --db oupafamilly --out /backup/\$(date +%Y%m%d)
\`\`\`

### Mise à jour
\`\`\`bash
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && yarn install && yarn build
sudo supervisorctl restart all
\`\`\`

## Support
- Architecture: React + FastAPI + MongoDB
- Compatible: Ubuntu 18.04+, Debian 10+
- Ports: 3000 (frontend), 8001 (backend), 27017 (mongo)
EOF

# 8. Optimiser package.json pour production
cd /app/frontend

# Ajouter scripts de production s'ils n'existent pas
npm pkg set scripts.start:prod="serve -s build -l 3000"
npm pkg set scripts.deploy="yarn build && yarn start:prod"

echo "✅ OPTIMISATION OVH TERMINÉE!"
echo ""
echo "📋 FICHIERS CRÉÉS:"
echo "   - docker-compose.yml (déployement container)"
echo "   - backend/Dockerfile"  
echo "   - frontend/Dockerfile"
echo "   - start_ovh.sh (script démarrage)"
echo "   - nginx.conf (configuration proxy)"
echo "   - DEPLOYMENT_OVH.md (documentation)"
echo "   - .env.example (templates configuration)"
echo ""
echo "🚀 PRÊT POUR DÉPLOYEMENT OVH!"
echo "📖 Voir DEPLOYMENT_OVH.md for instructions détaillées"