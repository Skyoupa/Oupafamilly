#!/usr/bin/env python3
"""
Script de téléchargement et stockage des images de tutoriels
"""

import requests
import os
import shutil
from pathlib import Path

# Images professionnelles à télécharger
IMAGES_TO_DOWNLOAD = {
    'gaming_setup.jpg': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzNDE1MDM2fDA&ixlib=rb-4.1.0&q=85',
    'esports_pro.jpg': 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwzfHxnYW1pbmd8ZW58MHx8fHwxNzUzNDE1MDM2fDA&ixlib=rb-4.1.0&q=85',
    'fps_gaming.jpg': 'https://images.unsplash.com/photo-1534423861386-85a16f5d13fd?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHw0fHxnYW1pbmd8ZW58MHx8fHwxNzUzNDE1MDM2fDA&ixlib=rb-4.1.0&q=85',
    'gaming_keyboard.jpg': 'https://images.unsplash.com/photo-1636036824578-d0d300a4effb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwyfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ4NDM5M3ww&ixlib=rb-4.1.0&q=85',
    'tournament.jpg': 'https://images.unsplash.com/photo-1587095951604-b9d924a3fda0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ4NDM5M3ww&ixlib=rb-4.1.0&q=85',
    'pro_area.jpg': 'https://images.unsplash.com/photo-1633545495735-25df17fb9f31?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHw0fHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ4NDM5M3ww&ixlib=rb-4.1.0&q=85',
    'cs2_setup.jpg': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzNDE1MDM2fDA&ixlib=rb-4.1.0&q=85',
    'wow_fantasy.jpg': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxmYW50YXN5fGVufDB8fHx8MTc1MzM5NzI4OHww&ixlib=rb-4.1.0&q=85',
    'lol_moba.jpg': 'https://images.unsplash.com/photo-1593280359364-5242f1958068?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    'sc2_strategy.jpg': 'https://images.unsplash.com/photo-1504370164829-8c6ef0c41d06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    'minecraft_creative.jpg': 'https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxNaW5lY3JhZnR8ZW58MHx8fHwxNzUzMzk3Mjg4fDA&ixlib=rb-4.1.0&q=85'
}

def download_image(url, filename, destination_dir):
    """Télécharge une image depuis une URL."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        file_path = destination_dir / filename
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        
        print(f"✅ Image téléchargée: {filename}")
        return True
    except Exception as e:
        print(f"❌ Erreur téléchargement {filename}: {str(e)}")
        return False

def main():
    print("📥 Téléchargement des images de tutoriels...")
    
    # Créer le répertoire de destination
    destination_dir = Path('/app/frontend/public/images/tutorials')
    destination_dir.mkdir(parents=True, exist_ok=True)
    
    # Télécharger toutes les images
    successful_downloads = 0
    total_images = len(IMAGES_TO_DOWNLOAD)
    
    for filename, url in IMAGES_TO_DOWNLOAD.items():
        if download_image(url, filename, destination_dir):
            successful_downloads += 1
    
    print(f"\n🎉 Téléchargement terminé!")
    print(f"📊 Images téléchargées: {successful_downloads}/{total_images}")
    
    if successful_downloads == total_images:
        print("✅ Toutes les images ont été téléchargées avec succès!")
    else:
        print(f"⚠️ {total_images - successful_downloads} images n'ont pas pu être téléchargées")

if __name__ == "__main__":
    main()