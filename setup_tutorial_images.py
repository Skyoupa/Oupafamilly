#!/usr/bin/env python3
"""
Script pour télécharger et organiser les images de tutoriels
"""

import requests
import os
from pathlib import Path
import hashlib

def download_image(url, filename):
    """Télécharger une image depuis une URL"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {url}: {str(e)}")
        return False

def setup_tutorial_images():
    """Configurer toutes les images de tutoriels"""
    
    # Dossier de destination
    images_dir = Path("/app/frontend/public/images/tutorials")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print("🖼️  Configuration des images de tutoriels...")
    
    # Images professionnelles d'Unsplash
    images = {
        # Images génériques gaming
        "gaming_setup.jpg": "https://images.unsplash.com/photo-1617507171089-6cb9aa5add36?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "esports_pro.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "gaming_keyboard.jpg": "https://images.unsplash.com/photo-1636036824578-d0d300a4effb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "pro_area.jpg": "https://images.unsplash.com/photo-1633545495735-25df17fb9f31?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHw0fHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "gaming_microphone.jpg": "https://images.unsplash.com/photo-1552820081-00b3187b7a57?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        
        # CS2 spécifiques
        "cs2_team_strategy.jpg": "https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTR8fGVzcG9ydHN8ZW58MHx8MHx8fDA%3D&ixlib=rb-4.1.0&q=85",
        "cs2_map_analysis.jpg": "https://images.unsplash.com/photo-1614732484003-ef9881555dc3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8OHx8Z2FtaW5nfGVufDB8fDB8fHww&ixlib=rb-4.1.0&q=85",
        "cs2_economy.jpg": "https://images.unsplash.com/photo-1511512578047-dfb367046420?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTJ8fGdhbWluZ3xlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "cs2_aim_training.jpg": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8Nnx8Z2FtaW5nfGVufDB8fDB8fHww&ixlib=rb-4.1.0&q=85",
        "cs2_utility.jpg": "https://images.unsplash.com/photo-1591123668439-5a70d3b15cf2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTZ8fGdhbWluZ3xlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "cs2_communication.jpg": "https://images.unsplash.com/photo-1621419483938-31fa5dc28bdf?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTh8fGdhbWluZ3xlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        
        # WoW spécifiques  
        "wow_classes.jpg": "https://images.unsplash.com/photo-1547036967-23d11aacaee0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8M3x8ZmFudGFzeXxlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "wow_dungeons.jpg": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8NXx8ZmFudGFzeXxlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "wow_raids.jpg": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8N3x8ZmFudGFzeXxlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "wow_pvp.jpg": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTJ8fGZhbnRhc3l8ZW58MHx8MHx8fDA%3D&ixlib=rb-4.1.0&q=85",
        "wow_economy.jpg": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8N3x8ZmFudGFzeXxlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "wow_guild.jpg": "https://images.unsplash.com/photo-1547036967-23d11aacaee0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8M3x8ZmFudGFzeXxlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        
        # LoL spécifiques
        "lol_lasthit.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "lol_vision.jpg": "https://images.unsplash.com/photo-1636036824578-d0d300a4effb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "lol_laning.jpg": "https://images.unsplash.com/photo-1633545495735-25df17fb9f31?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHw0fHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "lol_jungle.jpg": "https://images.unsplash.com/photo-1617507171089-6cb9aa5add36?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "lol_teamfight.jpg": "https://images.unsplash.com/photo-1552820081-00b3187b7a57?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "lol_macro.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        
        # SC2 spécifiques
        "sc2_economy.jpg": "https://images.unsplash.com/photo-1636036824578-d0d300a4effb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "sc2_units.jpg": "https://images.unsplash.com/photo-1633545495735-25df17fb9f31?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHw0fHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "sc2_scouting.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "sc2_micro.jpg": "https://images.unsplash.com/photo-1617507171089-6cb9aa5add36?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "sc2_expansion.jpg": "https://images.unsplash.com/photo-1552820081-00b3187b7a57?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "sc2_harass.jpg": "https://images.unsplash.com/photo-1636036824578-d0d300a4effb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwyfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        
        # Minecraft spécifiques
        "minecraft_survival.jpg": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8Nnx8Z2FtaW5nfGVufDB8fDB8fHww&ixlib=rb-4.1.0&q=85",
        "minecraft_building.jpg": "https://images.unsplash.com/photo-1511512578047-dfb367046420?crop=entropy&cs=srgb&fm=jpg&ixid=M3w0fHxzZWFyY2h8MTJ8fGdhbWluZ3xlbnwwfHwwfHx8MA%3D%3D&ixlib=rb-4.1.0&q=85",
        "minecraft_redstone.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHwxfHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85",
        "minecraft_exploration.jpg": "https://images.unsplash.com/photo-1617507171089-6cb9aa5add36?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "minecraft_nether.jpg": "https://images.unsplash.com/photo-1552820081-00b3187b7a57?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHxnYW1pbmclMjB0dXRvcmlhbHxlbnwwfHx8fDE3NTM0OTAzNjd8MA&ixlib=rb-4.1.0&q=85",
        "minecraft_enchanting.jpg": "https://images.unsplash.com/photo-1633545495735-25df17fb9f31?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzB8MHwxfHNlYXJjaHw0fHxlc3BvcnRzfGVufDB8fHx8MTc1MzQ5MDM3NHww&ixlib=rb-4.1.0&q=85"
    }
    
    # Télécharger toutes les images
    success_count = 0
    total_count = len(images)
    
    for filename, url in images.items():
        filepath = images_dir / filename
        if download_image(url, str(filepath)):
            success_count += 1
    
    print(f"\n📊 Résultats du téléchargement:")
    print(f"   ✅ Réussis: {success_count}/{total_count}")
    print(f"   📁 Dossier: {images_dir}")
    
    if success_count == total_count:
        print("🎉 Toutes les images ont été téléchargées avec succès!")
    else:
        print(f"⚠️  {total_count - success_count} images n'ont pas pu être téléchargées")
    
    return success_count == total_count

if __name__ == "__main__":
    print("🖼️  Téléchargement des images de tutoriels...")
    success = setup_tutorial_images()
    if success:
        print("✅ Configuration des images terminée!")
    else:
        print("❌ Certaines images n'ont pas pu être téléchargées")