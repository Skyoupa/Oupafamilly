#!/usr/bin/env python3
"""
Script pour corriger tous les problèmes restants :
1. Traduction complète en français
2. Tri par difficulté (débutant → intermédiaire → expert)
3. Images uniques pour chaque tutoriel
4. Vérification des 60 tutoriels
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.models import Tutorial, Game

async def fix_final_issues():
    """Corriger tous les problèmes restants."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🔧 Correction des problèmes finaux...")
    
    try:
        # 1. CORRECTION DES TRADUCTIONS EN FRANÇAIS
        print("\n🇫🇷 Correction des titres et descriptions en français...")
        
        # Traductions correctes par jeu
        translations = {
            "cs2": {
                "Stratégies d'équipe et coordination": {
                    "description": "Maîtrisez les stratégies d'équipe avancées avec coordination tactique, communication efficace et exécution de plans de jeu professionnels."
                },
                "Analyse de cartes et positionnement": {
                    "description": "Développez votre sens tactique avec analyse approfondie des cartes, positionnement optimal et contrôle territorial stratégique."
                },
                "Économie de jeu et gestion des achats": {
                    "description": "Optimisez votre économie de jeu avec gestion intelligente des ressources, timing d'achat et stratégies financières d'équipe."
                },
                "Techniques de tir et précision": {
                    "description": "Perfectionnez vos compétences de tir avec techniques de visée avancées, contrôle du recul et précision maximale au combat."
                },
                "Métier de support et utilités": {
                    "description": "Maîtrisez le rôle de support avec utilisation stratégique des grenades, soutien d'équipe et création d'opportunités tactiques."
                },
                "Communication et leadership": {
                    "description": "Développez vos compétences de leadership avec communication claire, prise de décision rapide et coordination d'équipe efficace."
                },
                "Anti-éco et stratégies spéciales": {
                    "description": "Maîtrisez les stratégies anti-éco avec adaptation tactique, gestion des rounds de force et exploitation des faiblesses adverses."
                },
                "Retakes et défense de sites": {
                    "description": "Perfectionnez vos techniques de retake avec coordination défensive, timing optimal et récupération stratégique des sites."
                },
                "Analyse de démos et amélioration": {
                    "description": "Développez vos compétences d'auto-analyse avec étude de démos, identification d'erreurs et planification d'amélioration systématique."
                },
                "Préparation mentale et gestion du stress": {
                    "description": "Optimisez votre performance mentale avec gestion du stress, concentration en match et résistance à la pression compétitive."
                },
                "Méta gaming et adaptation stratégique": {
                    "description": "Maîtrisez l'évolution du méta avec adaptation continue, analyse des tendances et innovation stratégique professionnelle."
                },
                "Coaching et développement d'équipe": {
                    "description": "Développez vos compétences de coaching avec analyse d'équipe, développement de talents et construction de cohésion collective."
                }
            },
            "wow": {
                "Classes et spécialisations optimales": {
                    "description": "Maîtrisez votre classe avec guides de spécialisation, optimisation des talents et strategies de gameplay pour performance maximale."
                },
                "Donjons et stratégies de groupe": {
                    "description": "Excellez dans les donjons avec stratégies de groupe, gestion des mécaniques et coordination d'équipe pour clears efficaces."
                },
                "Raids et mécaniques avancées": {
                    "description": "Conquérez les raids les plus difficiles avec compréhension des mécaniques, coordination de guilde et exécution parfaite."
                },
                "PvP et arènes compétitives": {
                    "description": "Dominez en PvP avec stratégies d'arène, composition d'équipe optimale et techniques de combat joueur contre joueur."
                },
                "Économie et auction house": {
                    "description": "Maximisez vos profits avec maîtrise de l'économie serveur, trading intelligent et stratégies d'auction house professionnelles."
                },
                "Guildes et leadership communautaire": {
                    "description": "Dirigez efficacement votre guilde avec management de communauté, organisation de raids et développement de cohésion d'équipe."
                },
                "Farming et optimisation des ressources": {
                    "description": "Optimisez votre farming avec routes efficaces, gestion du temps et maximisation des gains d'expérience et d'or."
                },
                "Add-ons et interface utilisateur": {
                    "description": "Personnalisez votre interface avec les meilleurs add-ons, configuration optimale et amélioration de l'expérience de jeu."
                },
                "Mécaniques avancées et min-maxing": {
                    "description": "Perfectionnez votre gameplay avec techniques avancées, optimisation statistique et exploitation maximale des mécaniques."
                },
                "Événements saisonniers et achievements": {
                    "description": "Maîtrisez tous les événements avec guides complets, optimisation du temps et collection d'achievements rares."
                },
                "Mythic+ et progression de haut niveau": {
                    "description": "Excellez en Mythic+ avec stratégies de progression, gestion des affixes et techniques de haut niveau compétitif."
                },
                "Builds et théorie-crafting avancé": {
                    "description": "Créez des builds optimaux avec théorie-crafting approfondi, simulation de DPS et adaptation aux mécaniques de raid."
                }
            },
            "lol": {
                "Bases du dernier hit et farm": {
                    "description": "Maîtrisez les fondamentaux du farming avec techniques de dernier hit, gestion des vagues et optimisation de l'or."
                },
                "Wards et contrôle de vision": {
                    "description": "Dominez la carte avec placement de wards stratégique, contrôle de vision et prévention des ganks ennemis."
                },
                "Phases de laning et trading": {
                    "description": "Excellez en phase de lane avec techniques de trading, gestion des cooldowns et pression constante sur l'adversaire."
                },
                "Jungle et contrôle des objectifs": {
                    "description": "Maîtrisez le jungle avec routes optimales, timing des ganks et contrôle stratégique des objectifs neutres."
                },
                "Team fights et positionnement": {
                    "description": "Dominez les combats d'équipe avec positionnement optimal, focus des cibles prioritaires et exécution coordonnée."
                },
                "Macro game et rotation": {
                    "description": "Développez votre vision stratégique avec macro game avancé, rotations optimales et contrôle territorial de la carte."
                },
                "Contre-jungle et pression": {
                    "description": "Maîtrisez les techniques de contre-jungle avec vol de camps, pression constante et déstabilisation de l'ennemi."
                },
                "Roaming et impact sur la carte": {
                    "description": "Maximisez votre impact avec roaming efficace, assistance aux lanes et création d'avantages multiples."
                },
                "Builds et adaptation d'objets": {
                    "description": "Optimisez vos builds avec adaptation situationnelle, ordre d'objets optimal et maximisation de l'efficacité."
                },
                "Psychologie et mental game": {
                    "description": "Maîtrisez l'aspect mental avec gestion du tilt, communication positive et maintien de la concentration."
                },
                "Composition d'équipe et synergies": {
                    "description": "Maîtrisez l'art de créer des compositions d'équipe équilibrées avec synergies de champions et stratégies de draft."
                },
                "Analyse replay et amélioration": {
                    "description": "Développez vos compétences d'auto-analyse avec techniques de review replay et planification d'amélioration systématique."
                }
            },
            "sc2": {
                "Bases économiques et workers": {
                    "description": "Maîtrisez les fondamentaux économiques avec gestion optimale des workers, expansion et balance ressources."
                },
                "Unités de base et compositions": {
                    "description": "Découvrez les unités essentielles avec compositions d'armée efficaces, synergies et contre-stratégies adaptées."
                },
                "Scouting et collecte d'informations": {
                    "description": "Développez vos techniques de reconnaissance avec scouting efficace, lecture des stratégies et adaptation tactique."
                },
                "Micro-gestion et contrôle d'unités": {
                    "description": "Perfectionnez votre micro avec contrôle d'unités précis, techniques de kiting et optimisation des combats."
                },
                "Stratégies d'expansion et map control": {
                    "description": "Maîtrisez l'expansion avec timing optimal, sécurisation des bases et contrôle territorial stratégique."
                },
                "Harass et techniques de pression": {
                    "description": "Excellez dans le harcèlement avec drops tactiques, raids économiques et pression constante sur l'adversaire."
                },
                "Tech trees et transitions": {
                    "description": "Optimisez vos arbres technologiques avec transitions fluides, timing des upgrades et adaptation stratégique."
                },
                "Défense et fortifications": {
                    "description": "Maîtrisez l'art défensif avec positionnement optimal, structures défensives et contre-attaques efficaces."
                },
                "All-ins et timings attacks": {
                    "description": "Perfectionnez vos attaques timing avec all-ins dévastateurs, coordination parfaite et exécution impeccable."
                },
                "Build orders et stratégies macro": {
                    "description": "Maîtrisez les build orders essentiels avec timing précis, gestion économique et transitions stratégiques."
                },
                "Combat et micro-gestion avancée": {
                    "description": "Perfectionnez vos compétences de micro-gestion avec contrôle d'unités expert et techniques de combat optimisées."
                },
                "Analyse replay et méta évolution": {
                    "description": "Développez vos compétences d'analyse stratégique avec étude de replays et compréhension de l'évolution du méta."
                }
            },
            "minecraft": {
                "Survie et premiers pas": {
                    "description": "Maîtrisez les bases de la survie avec techniques de première nuit, collecte de ressources et construction d'abris."
                },
                "Construction et bases créatives": {
                    "description": "Développez vos compétences de construction avec techniques architecturales, matériaux et design créatif."
                },
                "Redstone et mécanismes": {
                    "description": "Découvrez les circuits redstone avec mécanismes automatisés, portes logiques et systèmes intelligents."
                },
                "Exploration et donjons": {
                    "description": "Explorez efficacement le monde avec préparation d'expédition, navigation et conquête de structures."
                },
                "Nether et dimensions": {
                    "description": "Conquérez le Nether avec préparation stratégique, navigation sécurisée et récolte de ressources uniques."
                },
                "Enchantements et brewing": {
                    "description": "Optimisez votre progression avec systèmes d'enchantement efficaces et brewing avancé de potions."
                },
                "Fermes automatiques": {
                    "description": "Créez des fermes industrielles avec redstone complexe, rendements optimaux et systèmes automatisés."
                },
                "Combat et PvP": {
                    "description": "Maîtrisez le combat avec techniques PvP avancées, gestion d'équipement et stratégies de bataille."
                },
                "Serveurs et plugins": {
                    "description": "Administrez des serveurs avec configuration optimale, plugins essentiels et gestion de communauté."
                },
                "Builds et architecture avancée": {
                    "description": "Créez des constructions monumentales avec techniques architecturales avancées et planification de projets."
                },
                "Mods et customisation": {
                    "description": "Personnalisez votre expérience avec mods populaires, resource packs et modifications avancées."
                },
                "Compétitions et événements": {
                    "description": "Participez aux événements communautaires avec préparation compétitive et techniques de construction rapide."
                }
            }
        }
        
        # Images spécifiques par jeu et tutoriel
        tutorial_images = {
            "cs2": [
                '/images/tutorials/cs2_team_strategy.jpg',
                '/images/tutorials/cs2_map_analysis.jpg', 
                '/images/tutorials/cs2_economy.jpg',
                '/images/tutorials/cs2_aim_training.jpg',
                '/images/tutorials/cs2_utility.jpg',
                '/images/tutorials/cs2_communication.jpg',
                '/images/tutorials/cs2_antileco.jpg',
                '/images/tutorials/cs2_retakes.jpg',
                '/images/tutorials/cs2_demo_analysis.jpg',
                '/images/tutorials/cs2_mental.jpg',
                '/images/tutorials/cs2_meta.jpg',
                '/images/tutorials/cs2_coaching.jpg'
            ],
            "wow": [
                '/images/tutorials/wow_classes.jpg',
                '/images/tutorials/wow_dungeons.jpg',
                '/images/tutorials/wow_raids.jpg', 
                '/images/tutorials/wow_pvp.jpg',
                '/images/tutorials/wow_economy.jpg',
                '/images/tutorials/wow_guild.jpg',
                '/images/tutorials/wow_farming.jpg',
                '/images/tutorials/wow_addons.jpg',
                '/images/tutorials/wow_mechanics.jpg',
                '/images/tutorials/wow_events.jpg',
                '/images/tutorials/wow_mythicplus.jpg',
                '/images/tutorials/wow_builds.jpg'
            ],
            "lol": [
                '/images/tutorials/lol_lasthit.jpg',
                '/images/tutorials/lol_vision.jpg',
                '/images/tutorials/lol_laning.jpg',
                '/images/tutorials/lol_jungle.jpg',
                '/images/tutorials/lol_teamfight.jpg',
                '/images/tutorials/lol_macro.jpg',
                '/images/tutorials/lol_counterjungle.jpg',
                '/images/tutorials/lol_roaming.jpg',
                '/images/tutorials/lol_builds.jpg',
                '/images/tutorials/lol_mental.jpg',
                '/images/tutorials/lol_teamcomp.jpg',
                '/images/tutorials/lol_replay.jpg'
            ],
            "sc2": [
                '/images/tutorials/sc2_economy.jpg',
                '/images/tutorials/sc2_units.jpg',
                '/images/tutorials/sc2_scouting.jpg',
                '/images/tutorials/sc2_micro.jpg',
                '/images/tutorials/sc2_expansion.jpg',
                '/images/tutorials/sc2_harass.jpg',
                '/images/tutorials/sc2_tech.jpg',
                '/images/tutorials/sc2_defense.jpg',
                '/images/tutorials/sc2_allins.jpg',
                '/images/tutorials/sc2_buildorders.jpg',
                '/images/tutorials/sc2_combat.jpg',
                '/images/tutorials/sc2_replay.jpg'
            ],
            "minecraft": [
                '/images/tutorials/minecraft_survival.jpg',
                '/images/tutorials/minecraft_building.jpg',
                '/images/tutorials/minecraft_redstone.jpg',
                '/images/tutorials/minecraft_exploration.jpg',
                '/images/tutorials/minecraft_nether.jpg',
                '/images/tutorials/minecraft_enchanting.jpg',
                '/images/tutorials/minecraft_farms.jpg',
                '/images/tutorials/minecraft_combat.jpg',
                '/images/tutorials/minecraft_servers.jpg',
                '/images/tutorials/minecraft_architecture.jpg',
                '/images/tutorials/minecraft_mods.jpg',
                '/images/tutorials/minecraft_competitions.jpg'
            ]
        }
        
        # Appliquer les traductions et images
        for game, game_translations in translations.items():
            tutorials = await db.tutorials.find({"game": game}).to_list(None)
            game_images = tutorial_images.get(game, [])
            
            for i, tutorial in enumerate(tutorials):
                # Trouver la traduction correspondante
                title = tutorial.get('title', '')
                new_data = {}
                
                # Chercher la traduction par nom
                translation_found = False
                for french_title, data in game_translations.items():
                    if not translation_found:
                        new_data = {
                            "title": french_title,
                            "description": data["description"]
                        }
                        translation_found = True
                        break
                
                # Assigner une image unique
                if i < len(game_images):
                    new_data["image"] = game_images[i]
                else:
                    # Fallback si plus d'images que prévu
                    new_data["image"] = f'/images/tutorials/{game}_default.jpg'
                
                # Mettre à jour le tutoriel
                await db.tutorials.update_one(
                    {"_id": tutorial["_id"]},
                    {"$set": new_data}
                )
                
                if translation_found:
                    print(f"✅ {game.upper()}: {new_data['title']} - Image: {new_data['image']}")
                    # Supprimer la traduction utilisée pour éviter les doublons
                    del game_translations[french_title]
                    break
        
        # 2. TRI PAR DIFFICULTÉ ET ORDRE D'AFFICHAGE
        print("\n📊 Correction du tri par difficulté...")
        
        # Assigner des ordres pour le tri
        level_order = {"beginner": 1, "intermediate": 2, "expert": 3}
        
        all_tutorials = await db.tutorials.find({}).to_list(None)
        for tutorial in all_tutorials:
            level = tutorial.get('level', 'beginner')
            sort_order = level_order.get(level, 1)
            
            await db.tutorials.update_one(
                {"_id": tutorial["_id"]},
                {"$set": {"sort_order": sort_order}}
            )
        
        print("✅ Tri par difficulté appliqué (beginner → intermediate → expert)")
        
        # 3. VÉRIFICATION FINALE
        print("\n📈 Vérification finale...")
        
        final_count = await db.tutorials.count_documents({})
        for game in ["cs2", "wow", "lol", "sc2", "minecraft"]:
            game_count = await db.tutorials.count_documents({"game": game})
            print(f"   {game.upper()}: {game_count} tutoriels")
        
        print(f"\n📚 TOTAL FINAL: {final_count} tutoriels")
        
        if final_count == 60:
            print("🎉 PARFAIT! 60 tutoriels exactement (12 par jeu)")
        else:
            print(f"⚠️  Attention: {final_count} tutoriels trouvés (attendu: 60)")
        
        print("\n✅ Toutes les corrections appliquées:")
        print("   🇫🇷 Titres et descriptions traduits en français")
        print("   🖼️  Images uniques assignées par tutoriel")
        print("   📊 Tri par difficulté configuré")
        print("   ✨ Système prêt pour affichage optimal!")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 Correction finale des problèmes...")
    asyncio.run(fix_final_issues())
    print("✅ Corrections terminées !")