# Déployement Oupafamilly sur OVH

## Prérequis
- Serveur VPS/dédié OVH avec Ubuntu/Debian
- Node.js 16+
- Python 3.9+
- MongoDB 4.4+
- Nginx (optionnel)

## Installation Rapide

### 1. Cloner le projet
```bash
git clone <your-repo-url>
cd oupafamilly
```

### 2. Configuration
```bash
# Copier les fichiers d'exemple
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Modifier les variables selon votre environnement
nano backend/.env
nano frontend/.env
```

### 3. Démarrage automatique
```bash
chmod +x start_ovh.sh
./start_ovh.sh
```

### 4. Avec Docker (recommandé)
```bash
docker-compose up -d
```

## Configuration Production

### Variables d'environnement
- `MONGO_URL`: URL MongoDB (ex: mongodb://localhost:27017/oupafamilly)
- `REACT_APP_BACKEND_URL`: URL backend (ex: https://yourdomain.com/api)
- `JWT_SECRET`: Clé secrète JWT (générer une clé forte)

### Nginx (optionnel)
```bash
sudo cp nginx.conf /etc/nginx/sites-available/oupafamilly
sudo ln -s /etc/nginx/sites-available/oupafamilly /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Maintenance

### Backup base de données
```bash
mongodump --db oupafamilly --out /backup/$(date +%Y%m%d)
```

### Mise à jour
```bash
git pull origin main
cd backend && pip install -r requirements.txt
cd ../frontend && yarn install && yarn build
sudo supervisorctl restart all
```

## Support
- Architecture: React + FastAPI + MongoDB
- Compatible: Ubuntu 18.04+, Debian 10+
- Ports: 3000 (frontend), 8001 (backend), 27017 (mongo)
