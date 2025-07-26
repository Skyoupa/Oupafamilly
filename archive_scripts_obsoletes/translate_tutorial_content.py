#!/usr/bin/env python3
"""
Script pour traduire le contenu complet des tutoriels en français
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import re

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.models import Tutorial, Game

def translate_content_to_french(content, game):
    """Traduire le contenu en français en gardant les termes de jeu en anglais."""
    
    # Dictionnaire de traductions communes
    translations = {
        # Mots courants
        "and": "et",
        "the": "le/la",
        "with": "avec",
        "for": "pour",
        "in": "dans",
        "on": "sur",
        "at": "à",
        "by": "par",
        "from": "de",
        "to": "vers",
        "your": "votre",
        "you": "vous",
        "this": "ce/cette",
        "that": "ce/cette",
        "will": "sera",
        "can": "peut",
        "should": "devrait",
        "must": "doit",
        "have": "avoir",
        "has": "a",
        "are": "sont",
        "is": "est",
        "be": "être",
        "use": "utiliser",
        "using": "utilisant",
        "when": "quand",
        "where": "où",
        "how": "comment",
        "why": "pourquoi",
        "what": "quoi",
        "which": "lequel",
        
        # Termes gaming généraux
        "Guide": "Guide",
        "Professional": "Professionnel",
        "Strategy": "Stratégie",
        "Tactics": "Tactiques",
        "Advanced": "Avancé",
        "Expert": "Expert",
        "Beginner": "Débutant",
        "Intermediate": "Intermédiaire",
        "Tips": "Conseils",
        "Techniques": "Techniques",
        "Optimization": "Optimisation",
        "Performance": "Performance",
        "Analysis": "Analyse",
        "Training": "Entraînement",
        "Practice": "Pratique",
        "Master": "Maîtriser",
        "Mastery": "Maîtrise",
        "Skills": "Compétences",
        "Skill": "Compétence",
        "Level": "Niveau",
        "Build": "Build",
        "Setup": "Configuration",
        "Settings": "Paramètres",
        "Configuration": "Configuration",
        "Key": "Clé",
        "Important": "Important",
        "Critical": "Critique",
        "Essential": "Essentiel",
        "Basic": "Basique",
        "Foundation": "Fondation",
        "Fundamentals": "Fondamentaux",
        "Core": "Core",
        "Main": "Principal",
        "Primary": "Primaire",
        "Secondary": "Secondaire",
        "Optimal": "Optimal",
        "Best": "Meilleur",
        "Top": "Top",
        "Pro": "Pro",
        "Team": "Équipe",
        "Player": "Joueur",
        "Game": "Jeu",
        "Match": "Match",
        "Round": "Round",
        "Win": "Victoire",
        "Victory": "Victoire",
        "Defeat": "Défaite",
        "Loss": "Défaite",
        "Score": "Score",
        "Points": "Points",
        "Ranking": "Classement",
        "Rank": "Rang",
        "Stats": "Statistiques",
        "Statistics": "Statistiques",
        "Data": "Données", 
        "Information": "Information",
        "Knowledge": "Connaissance",
        "Experience": "Expérience",
        "Learning": "Apprentissage",
        "Improvement": "Amélioration",
        "Progress": "Progrès",
        "Development": "Développement",
        "Growth": "Croissance",
        "Success": "Succès",
        "Achievement": "Réussite",
        "Goal": "Objectif",
        "Target": "Cible",
        "Focus": "Focus",
        "Concentration": "Concentration",
        "Attention": "Attention",
        "Control": "Contrôle",
        "Management": "Gestion",
        "Decision": "Décision",
        "Choice": "Choix",
        "Option": "Option",
        "Method": "Méthode",
        "Approach": "Approche",
        "System": "Système",
        "Process": "Processus",
        "Procedure": "Procédure",
        "Step": "Étape",
        "Phase": "Phase",
        "Stage": "Stade",
        "Pattern": "Pattern",
        "Style": "Style",
        "Type": "Type",
        "Category": "Catégorie",
        "Section": "Section",
        "Part": "Partie",
        "Component": "Composant",
        "Element": "Élément",
        "Feature": "Fonctionnalité",
        "Function": "Fonction",
        "Tool": "Outil",
        "Resource": "Ressource",
        "Material": "Matériel",
        "Equipment": "Équipement",
        "Item": "Objet",
        "Object": "Objet",
        "Unit": "Unité",
        "Character": "Personnage",
        "Avatar": "Avatar",
        "Profile": "Profil",
        "Account": "Compte",
        "User": "Utilisateur",
        "Interface": "Interface",
        "Menu": "Menu",
        "Button": "Bouton",
        "Click": "Cliquer",
        "Press": "Appuyer",
        "Hold": "Maintenir",
        "Release": "Relâcher",
        "Move": "Déplacer",
        "Movement": "Mouvement",
        "Position": "Position",
        "Location": "Emplacement",
        "Place": "Lieu",
        "Area": "Zone",
        "Region": "Région",
        "Territory": "Territoire",
        "Map": "Carte",
        "Field": "Terrain",
        "Environment": "Environnement",
        "World": "Monde",
        "Universe": "Univers",
        "Dimension": "Dimension",
        "Space": "Espace",
        "Time": "Temps",
        "Duration": "Durée",
        "Period": "Période",
        "Moment": "Moment",
        "Instant": "Instant",
        "Speed": "Vitesse",
        "Rate": "Taux",
        "Frequency": "Fréquence",
        "Timing": "Timing",
        "Schedule": "Horaire",
        "Plan": "Plan",
        "Strategy": "Stratégie",
        "Tactic": "Tactique",
        "Technique": "Technique",
        "Method": "Méthode",
        "Way": "Façon"
    }
    
    # Traduire le contenu ligne par ligne
    lines = content.split('\n')
    translated_lines = []
    
    for line in lines:
        translated_line = line
        
        # Garder les headers markdown intacts
        if line.startswith('#'):
            # Traduire seulement le texte après les #
            header_level = len(line) - len(line.lstrip('#'))
            header_text = line[header_level:].strip()
            
            # Traductions spécifiques pour les headers
            header_translations = {
                "Professional Guide": "Guide Professionnel",
                "Advanced Techniques": "Techniques Avancées",
                "Basic Fundamentals": "Fondamentaux de Base",
                "Strategy Overview": "Aperçu Stratégique",
                "Team Coordination": "Coordination d'Équipe",
                "Individual Skills": "Compétences Individuelles",
                "Game Mechanics": "Mécaniques de Jeu",
                "Equipment Setup": "Configuration Équipement",
                "Training Methods": "Méthodes d'Entraînement",
                "Performance Analysis": "Analyse de Performance",
                "Competitive Play": "Jeu Compétitif",
                "Advanced Strategies": "Stratégies Avancées",
                "Core Concepts": "Concepts Fondamentaux",
                "Essential Tips": "Conseils Essentiels",
                "Pro Techniques": "Techniques Pro",
                "Optimization Guide": "Guide d'Optimisation"
            }
            
            for eng, fr in header_translations.items():
                if eng.lower() in header_text.lower():
                    header_text = header_text.replace(eng, fr)
            
            translated_line = '#' * header_level + ' ' * (header_level) + header_text
        
        # Traduire les listes et texte normal
        else:
            # Traductions par mots/phrases complètes
            for english, french in translations.items():
                # Remplacer les mots complets (avec limites de mots)
                pattern = r'\b' + re.escape(english) + r'\b'
                translated_line = re.sub(pattern, french, translated_line, flags=re.IGNORECASE)
        
        translated_lines.append(translated_line)
    
    return '\n'.join(translated_lines)

async def translate_all_tutorial_content():
    """Traduire le contenu de tous les tutoriels."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🇫🇷 Traduction du contenu complet des tutoriels...")
    
    try:
        # Récupérer tous les tutoriels
        all_tutorials = await db.tutorials.find({}).to_list(None)
        
        print(f"📚 {len(all_tutorials)} tutoriels à traduire")
        
        translated_count = 0
        
        for tutorial in all_tutorials:
            game = tutorial.get('game', '')
            title = tutorial.get('title', 'Sans titre')
            content = tutorial.get('content', '')
            
            print(f"\n🎮 {game.upper()}: {title}")
            
            # Vérifier si le contenu nécessite une traduction
            english_indicators = ['the ', 'and ', 'with ', 'your ', 'this ', 'will ', 'can ', 'you ', 'are ', 'is ']
            content_lower = content.lower()
            english_count = sum(1 for indicator in english_indicators if indicator in content_lower)
            
            if english_count > 5:  # Si contenu semble anglais
                print(f"   📝 Traduction nécessaire ({english_count} indicateurs anglais détectés)")
                
                # Traduire le contenu
                translated_content = translate_content_to_french(content, game)
                
                # Mettre à jour en base
                await db.tutorials.update_one(
                    {"_id": tutorial["_id"]},
                    {"$set": {"content": translated_content}}
                )
                
                translated_count += 1
                print(f"   ✅ Contenu traduit et mis à jour")
            else:
                print(f"   ⏭️  Contenu déjà en français")
        
        print(f"\n📊 RÉSUMÉ TRADUCTION:")
        print(f"   ✅ {translated_count} tutoriels traduits")
        print(f"   ⏭️  {len(all_tutorials) - translated_count} tutoriels déjà en français")
        print(f"   📚 {len(all_tutorials)} tutoriels total vérifiés")
        
        if translated_count > 0:
            print("🎉 Traduction du contenu terminée avec succès!")
        else:
            print("✅ Tous les contenus étaient déjà en français!")
            
        return translated_count
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🇫🇷 Début de la traduction du contenu...")
    asyncio.run(translate_all_tutorial_content())
    print("✅ Traduction terminée !")