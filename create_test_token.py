import asyncio
from datetime import datetime, timedelta
from jose import jwt
import os

# Configuration identique à celle du backend
SECRET_KEY = "jwt-secret-for-oupafamilly-community-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 jours

async def create_test_token():
    """
    Créer un token de test pour accéder aux fonctionnalités communautaires
    """
    
    print("🔑 Création d'un token de test pour les fonctionnalités communautaires...")
    
    # Données du token (utiliser l'admin par défaut)
    token_data = {
        "sub": "admin@oupafamilly.com",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow()
    }
    
    # Créer le token
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    print(f"✅ Token de test créé avec succès !")
    print(f"📧 Email: admin@oupafamilly.com")
    print(f"⏰ Expire dans: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes ({ACCESS_TOKEN_EXPIRE_MINUTES // (60*24)} jours)")
    print()
    print("🚀 Pour tester l'interface communauté :")
    print("1. Ouvrez votre navigateur et allez sur http://localhost:3000/community")
    print("2. Ouvrez les outils de développement (F12)")
    print("3. Dans la console, tapez :")
    print(f'   localStorage.setItem("token", "{access_token}")')
    print("4. Rechargez la page")
    print()
    print("💡 Token à copier :")
    print(f"{access_token}")
    
    return access_token

if __name__ == '__main__':
    asyncio.run(create_test_token())