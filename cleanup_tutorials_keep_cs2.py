#!/usr/bin/env python3
"""
Script pour nettoyer les tutoriels : ne garder que CS2 et les classer par difficulté
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def cleanup_tutorials():
    """Supprimer tous les tutoriels sauf CS2 et classer les CS2 par difficulté."""
    
    # Load environment variables
    load_dotenv('/app/backend/.env')
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ MONGO_URL non trouvé dans les variables d'environnement")
        return
    
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get('DB_NAME', 'oupafamilly')
    db = client[db_name]
    
    try:
        print("🚀 Début du nettoyage des tutoriels...")
        
        # 1. Compter les tutoriels avant nettoyage
        total_before = await db.tutorials.count_documents({})
        cs2_before = await db.tutorials.count_documents({"game": "cs2"})
        other_games_before = total_before - cs2_before
        
        print(f"📊 État actuel :")
        print(f"   Total tutoriels : {total_before}")
        print(f"   Tutoriels CS2 : {cs2_before}")
        print(f"   Autres jeux : {other_games_before}")
        
        # 2. Supprimer tous les tutoriels sauf CS2
        print("\n🗑️ Suppression des tutoriels non-CS2...")
        delete_result = await db.tutorials.delete_many({
            "game": {"$ne": "cs2"}
        })
        print(f"   ✅ {delete_result.deleted_count} tutoriels supprimés")
        
        # 3. Récupérer tous les tutoriels CS2 et les analyser
        print("\n📋 Analyse des tutoriels CS2 restants...")
        cs2_tutorials = await db.tutorials.find({"game": "cs2"}).to_list(None)
        
        if not cs2_tutorials:
            print("   ❌ Aucun tutoriel CS2 trouvé !")
            return
        
        print(f"   📚 {len(cs2_tutorials)} tutoriels CS2 trouvés")
        
        # 4. Classer par difficulté et mettre à jour sort_order
        difficulty_map = {
            "beginner": 1,
            "intermediate": 2, 
            "expert": 3
        }
        
        difficulty_counts = {"beginner": 0, "intermediate": 0, "expert": 0}
        updated_count = 0
        
        for tutorial in cs2_tutorials:
            level = tutorial.get("level", "beginner").lower()
            if level not in difficulty_map:
                level = "beginner"  # Par défaut
            
            difficulty_counts[level] += 1
            expected_sort_order = difficulty_map[level]
            current_sort_order = tutorial.get("sort_order")
            
            # Mettre à jour si sort_order incorrect ou manquant
            if current_sort_order != expected_sort_order:
                await db.tutorials.update_one(
                    {"id": tutorial["id"]},
                    {"$set": {"sort_order": expected_sort_order}}
                )
                updated_count += 1
                print(f"   📝 Mis à jour : '{tutorial.get('title', 'Sans titre')}' -> sort_order={expected_sort_order}")
        
        print(f"\n✅ Classification terminée :")
        print(f"   🔰 Débutant (sort_order=1) : {difficulty_counts['beginner']} tutoriels")
        print(f"   🔶 Intermédiaire (sort_order=2) : {difficulty_counts['intermediate']} tutoriels")
        print(f"   🔴 Expert (sort_order=3) : {difficulty_counts['expert']} tutoriels")
        print(f"   📊 {updated_count} tutoriels mis à jour avec sort_order")
        
        # 5. Vérification finale
        total_after = await db.tutorials.count_documents({})
        print(f"\n🎯 Résultat final :")
        print(f"   Total tutoriels après nettoyage : {total_after}")
        print(f"   Tutoriels supprimés : {total_before - total_after}")
        
        # 6. Afficher quelques exemples de tutoriels classés
        print(f"\n📖 Exemples de tutoriels CS2 classés :")
        
        # Débutant
        beginner_tutorials = await db.tutorials.find({
            "game": "cs2", 
            "level": "beginner"
        }).sort("sort_order", 1).limit(3).to_list(3)
        
        if beginner_tutorials:
            print("   🔰 DÉBUTANT :")
            for tuto in beginner_tutorials:
                print(f"      - {tuto.get('title', 'Sans titre')} (sort_order: {tuto.get('sort_order', 'N/A')})")
        
        # Intermédiaire
        intermediate_tutorials = await db.tutorials.find({
            "game": "cs2", 
            "level": "intermediate"
        }).sort("sort_order", 1).limit(3).to_list(3)
        
        if intermediate_tutorials:
            print("   🔶 INTERMÉDIAIRE :")
            for tuto in intermediate_tutorials:
                print(f"      - {tuto.get('title', 'Sans titre')} (sort_order: {tuto.get('sort_order', 'N/A')})")
        
        # Expert
        expert_tutorials = await db.tutorials.find({
            "game": "cs2", 
            "level": "expert"
        }).sort("sort_order", 1).limit(3).to_list(3)
        
        if expert_tutorials:
            print("   🔴 EXPERT :")
            for tuto in expert_tutorials:
                print(f"      - {tuto.get('title', 'Sans titre')} (sort_order: {tuto.get('sort_order', 'N/A')})")
        
        print(f"\n🎉 Nettoyage terminé avec succès !")
        print(f"✅ Seuls les tutoriels CS2 ont été conservés")
        print(f"✅ Tous les tutoriels CS2 sont classés par difficulté (sort_order)")
        print(f"✅ Base de données optimisée pour focus CS2 uniquement")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage : {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🔧 Nettoyage des tutoriels - Conservation CS2 uniquement...")
    asyncio.run(cleanup_tutorials())
    print("🎯 Nettoyage terminé !")