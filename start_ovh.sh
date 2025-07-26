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
