"""
💰 SYSTÈME PREMIUM ÉLITE - MONÉTISATION OUPAFAMILLY
Abonnements premium avec Stripe et fonctionnalités exclusives
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from auth import get_current_user, get_admin_user
from database import db
from monitoring import app_logger, log_user_action
import stripe
import os
from enum import Enum
import uuid

# Configuration Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')

router = APIRouter(prefix="/premium", tags=["Premium System"])

# ===============================================
# MODÈLES PREMIUM
# ===============================================

class PremiumTier(str, Enum):
    BASIC = "basic"
    ELITE = "elite"
    LEGEND = "legend"

class PremiumPlan(BaseModel):
    id: str
    name: str
    tier: PremiumTier
    price_monthly: int  # en centimes
    price_yearly: int   # en centimes
    features: List[str]
    stripe_price_id_monthly: str
    stripe_price_id_yearly: str
    max_custom_themes: int
    analytics_retention_days: int
    support_priority: str
    exclusive_badges: List[str]

class SubscriptionRequest(BaseModel):
    plan_id: str
    billing_period: str  # "monthly" ou "yearly"
    payment_method_id: str

class PremiumFeatureUsage(BaseModel):
    feature_name: str
    usage_count: int
    limit: int
    reset_date: datetime

# ===============================================
# CONFIGURATION DES PLANS PREMIUM
# ===============================================

PREMIUM_PLANS = {
    "basic": PremiumPlan(
        id="basic",
        name="Oupafamilly Basic",
        tier=PremiumTier.BASIC,
        price_monthly=499,  # 4.99€
        price_yearly=4999,  # 49.99€ (2 mois gratuits)
        features=[
            "🎨 1 thème personnalisé",
            "📊 Statistiques avancées (30 jours)",
            "🏅 Badge 'Supporter'", 
            "💬 Support prioritaire",
            "🚫 Publicités supprimées"
        ],
        stripe_price_id_monthly="price_basic_monthly",
        stripe_price_id_yearly="price_basic_yearly",
        max_custom_themes=1,
        analytics_retention_days=30,
        support_priority="standard",
        exclusive_badges=["supporter"]
    ),
    
    "elite": PremiumPlan(
        id="elite",
        name="Oupafamilly Elite",
        tier=PremiumTier.ELITE,
        price_monthly=999,  # 9.99€
        price_yearly=9999,  # 99.99€
        features=[
            "🎨 3 thèmes personnalisés",
            "📊 Statistiques avancées (90 jours)",
            "🏅 Badge 'Elite' + animations",
            "💬 Support prioritaire rapide",
            "🚫 Publicités supprimées",
            "🎯 Analyses de performance détaillées",
            "⚡ Accès anticipé aux nouvelles fonctionnalités",
            "🎪 Avatar animé personnalisé"
        ],
        stripe_price_id_monthly="price_elite_monthly", 
        stripe_price_id_yearly="price_elite_yearly",
        max_custom_themes=3,
        analytics_retention_days=90,
        support_priority="high",
        exclusive_badges=["elite", "early_access"]
    ),
    
    "legend": PremiumPlan(
        id="legend",
        name="Oupafamilly Legend",
        tier=PremiumTier.LEGEND,
        price_monthly=1999,  # 19.99€
        price_yearly=19999,  # 199.99€
        features=[
            "🎨 Thèmes illimités + créateur de thèmes",
            "📊 Statistiques avancées (1 an)",
            "🏅 Badge 'Legend' exclusif avec effets",
            "💬 Support prioritaire VIP (< 2h)",
            "🚫 Publicités supprimées",
            "🎯 Analyses de performance complètes",
            "⚡ Accès anticipé + beta testing",
            "🎪 Avatar animé + bannière personnalisée",
            "👑 Rôle spécial dans Discord",
            "🎁 Coins bonus quotidiens (+200)",
            "🏆 Tournois privés Legend",
            "📈 API personnelle pour ses stats"
        ],
        stripe_price_id_monthly="price_legend_monthly",
        stripe_price_id_yearly="price_legend_yearly", 
        max_custom_themes=999,
        analytics_retention_days=365,
        support_priority="vip",
        exclusive_badges=["legend", "beta_tester", "vip"]
    )
}

# ===============================================
# ENDPOINTS PREMIUM
# ===============================================

@router.get("/plans")
async def get_premium_plans():
    """📋 Récupère tous les plans premium disponibles"""
    try:
        plans_data = []
        
        for plan_id, plan in PREMIUM_PLANS.items():
            plans_data.append({
                "id": plan.id,
                "name": plan.name,
                "tier": plan.tier,
                "pricing": {
                    "monthly": {
                        "amount": plan.price_monthly,
                        "formatted": f"{plan.price_monthly / 100:.2f}€"
                    },
                    "yearly": {
                        "amount": plan.price_yearly,
                        "formatted": f"{plan.price_yearly / 100:.2f}€",
                        "monthly_equivalent": f"{plan.price_yearly / 12 / 100:.2f}€/mois",
                        "savings": f"{((plan.price_monthly * 12 - plan.price_yearly) / 100):.2f}€"
                    }
                },
                "features": plan.features,
                "max_custom_themes": plan.max_custom_themes,
                "analytics_retention": f"{plan.analytics_retention_days} jours",
                "support_level": plan.support_priority,
                "exclusive_badges": plan.exclusive_badges
            })
        
        return {
            "plans": plans_data,
            "currency": "EUR",
            "trial_period": "7 jours gratuits",
            "popular_plan": "elite"
        }
        
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération plans premium: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des plans")

@router.post("/subscribe")
async def create_premium_subscription(
    request: SubscriptionRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """💳 Crée un abonnement premium avec Stripe"""
    try:
        if not stripe.api_key:
            raise HTTPException(
                status_code=503,
                detail="Service de paiement temporairement indisponible"
            )
        
        # Valider le plan
        if request.plan_id not in PREMIUM_PLANS:
            raise HTTPException(
                status_code=400,
                detail="Plan premium invalide"
            )
        
        plan = PREMIUM_PLANS[request.plan_id]
        
        # Vérifier si l'utilisateur n'a pas déjà un abonnement
        existing_subscription = await db.premium_subscriptions.find_one({
            "user_id": current_user['id'],
            "status": {"$in": ["active", "trialing"]}
        })
        
        if existing_subscription:
            raise HTTPException(
                status_code=409,
                detail="Vous avez déjà un abonnement actif"
            )
        
        # Récupérer ou créer le customer Stripe
        stripe_customer = await _get_or_create_stripe_customer(current_user)
        
        # Attacher la méthode de paiement
        try:
            stripe.PaymentMethod.attach(
                request.payment_method_id,
                customer=stripe_customer.id
            )
            
            # Définir comme méthode par défaut
            stripe.Customer.modify(
                stripe_customer.id,
                invoice_settings={'default_payment_method': request.payment_method_id}
            )
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erreur méthode de paiement: {str(e)}"
            )
        
        # Créer l'abonnement Stripe
        price_id = (
            plan.stripe_price_id_yearly if request.billing_period == "yearly" 
            else plan.stripe_price_id_monthly
        )
        
        try:
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[{'price': price_id}],
                trial_period_days=7,  # 7 jours gratuits
                metadata={
                    'user_id': current_user['id'],
                    'plan_id': request.plan_id,
                    'billing_period': request.billing_period
                }
            )
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erreur création abonnement: {str(e)}"
            )
        
        # Enregistrer l'abonnement en base
        subscription_data = {
            "id": str(uuid.uuid4()),
            "user_id": current_user['id'],
            "stripe_subscription_id": stripe_subscription.id,
            "stripe_customer_id": stripe_customer.id,
            "plan_id": request.plan_id,
            "billing_period": request.billing_period,
            "status": stripe_subscription.status,
            "current_period_start": datetime.fromtimestamp(stripe_subscription.current_period_start),
            "current_period_end": datetime.fromtimestamp(stripe_subscription.current_period_end),
            "trial_end": datetime.fromtimestamp(stripe_subscription.trial_end) if stripe_subscription.trial_end else None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.premium_subscriptions.insert_one(subscription_data)
        
        # Activer les fonctionnalités premium
        background_tasks.add_task(
            _activate_premium_features,
            current_user['id'],
            request.plan_id
        )
        
        # Log de l'action
        log_user_action(current_user['id'], "premium_subscription_created", {
            "plan_id": request.plan_id,
            "billing_period": request.billing_period,
            "stripe_subscription_id": stripe_subscription.id
        })
        
        app_logger.info(f"💰 Nouvel abonnement premium: {current_user['username']} -> {request.plan_id}")
        
        return {
            "message": "Abonnement premium créé avec succès !",
            "subscription": {
                "id": subscription_data["id"],
                "plan": plan.name,
                "status": "trial" if stripe_subscription.trial_end else "active",
                "trial_end": subscription_data["trial_end"],
                "next_billing": subscription_data["current_period_end"],
                "features_activated": plan.features
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur création abonnement premium: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'abonnement")

@router.get("/my-subscription")
async def get_my_premium_subscription(current_user: dict = Depends(get_current_user)):
    """📊 Récupère l'abonnement premium de l'utilisateur"""
    try:
        subscription = await db.premium_subscriptions.find_one({
            "user_id": current_user['id'],
            "status": {"$in": ["active", "trialing", "past_due"]}
        })
        
        if not subscription:
            return {
                "has_premium": False,
                "message": "Aucun abonnement premium actif"
            }
        
        plan = PREMIUM_PLANS.get(subscription["plan_id"])
        if not plan:
            raise HTTPException(status_code=404, detail="Plan premium introuvable")
        
        # Calculer l'utilisation des fonctionnalités
        feature_usage = await _get_user_feature_usage(current_user['id'], plan)
        
        # Récupérer les badges premium
        premium_badges = await db.user_badges.find({
            "user_id": current_user['id'],
            "badge_id": {"$in": plan.exclusive_badges}
        }).to_list(None)
        
        return {
            "has_premium": True,
            "subscription": {
                "id": subscription["id"],
                "plan": {
                    "id": plan.id,
                    "name": plan.name,
                    "tier": plan.tier
                },
                "status": subscription["status"],
                "billing_period": subscription["billing_period"],
                "current_period_end": subscription["current_period_end"],
                "trial_end": subscription.get("trial_end"),
                "is_trial": subscription.get("trial_end") and datetime.utcnow() < subscription["trial_end"]
            },
            "features": {
                "custom_themes": {
                    "used": feature_usage.get("custom_themes", 0),
                    "limit": plan.max_custom_themes
                },
                "analytics_retention": plan.analytics_retention_days,
                "support_priority": plan.support_priority,
                "exclusive_badges": len(premium_badges)
            },
            "next_billing": subscription["current_period_end"],
            "can_cancel": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération abonnement: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de l'abonnement")

@router.post("/cancel")
async def cancel_premium_subscription(
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """❌ Annule l'abonnement premium"""
    try:
        subscription = await db.premium_subscriptions.find_one({
            "user_id": current_user['id'],
            "status": {"$in": ["active", "trialing"]}
        })
        
        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Aucun abonnement actif à annuler"
            )
        
        # Annuler dans Stripe
        try:
            stripe.Subscription.modify(
                subscription["stripe_subscription_id"],
                cancel_at_period_end=True
            )
            
        except stripe.error.StripeError as e:
            app_logger.error(f"Erreur annulation Stripe: {e}")
            # Continue même si Stripe échoue
        
        # Mettre à jour en base
        await db.premium_subscriptions.update_one(
            {"id": subscription["id"]},
            {
                "$set": {
                    "status": "canceled",
                    "canceled_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Programmer la désactivation des fonctionnalités
        background_tasks.add_task(
            _schedule_premium_deactivation,
            current_user['id'],
            subscription["current_period_end"]
        )
        
        # Log de l'action
        log_user_action(current_user['id'], "premium_subscription_canceled", {
            "subscription_id": subscription["id"],
            "plan_id": subscription["plan_id"]
        })
        
        return {
            "message": "Abonnement annulé avec succès",
            "details": "Vos fonctionnalités premium resteront actives jusqu'à la fin de la période de facturation",
            "access_until": subscription["current_period_end"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur annulation abonnement: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'annulation")

@router.get("/features")
async def get_premium_features(current_user: dict = Depends(get_current_user)):
    """🎯 Récupère les fonctionnalités premium accessibles"""
    try:
        # Vérifier l'abonnement
        subscription = await db.premium_subscriptions.find_one({
            "user_id": current_user['id'],
            "status": {"$in": ["active", "trialing"]}
        })
        
        if not subscription:
            return {
                "has_premium": False,
                "available_features": [],
                "upgrade_required": True
            }
        
        plan = PREMIUM_PLANS.get(subscription["plan_id"])
        if not plan:
            return {"has_premium": False, "error": "Plan introuvable"}
        
        # Fonctionnalités disponibles
        features = {
            "custom_themes": {
                "enabled": True,
                "limit": plan.max_custom_themes,
                "description": "Créez et utilisez des thèmes personnalisés"
            },
            "advanced_analytics": {
                "enabled": True,
                "retention_days": plan.analytics_retention_days,
                "description": "Accès aux statistiques avancées"
            },
            "priority_support": {
                "enabled": True,
                "level": plan.support_priority,
                "description": "Support prioritaire de l'équipe"
            },
            "exclusive_badges": {
                "enabled": True,
                "badges": plan.exclusive_badges,
                "description": "Badges exclusifs aux membres premium"
            },
            "ad_free": {
                "enabled": True,
                "description": "Expérience sans publicité"
            }
        }
        
        # Fonctionnalités spéciales par tier
        if plan.tier in [PremiumTier.ELITE, PremiumTier.LEGEND]:
            features["early_access"] = {
                "enabled": True,
                "description": "Accès anticipé aux nouvelles fonctionnalités"
            }
            features["animated_avatar"] = {
                "enabled": True,
                "description": "Avatar animé personnalisé"
            }
        
        if plan.tier == PremiumTier.LEGEND:
            features["bonus_coins"] = {
                "enabled": True,
                "daily_bonus": 200,
                "description": "Bonus quotidien de coins"
            }
            features["private_tournaments"] = {
                "enabled": True,
                "description": "Accès aux tournois privés Legend"
            }
            features["personal_api"] = {
                "enabled": True,
                "description": "API personnelle pour vos statistiques"
            }
        
        return {
            "has_premium": True,
            "plan": {
                "id": plan.id,
                "name": plan.name,
                "tier": plan.tier
            },
            "features": features,
            "subscription_status": subscription["status"]
        }
        
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération fonctionnalités premium: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des fonctionnalités")

@router.get("/usage")
async def get_premium_usage_stats(current_user: dict = Depends(get_current_user)):
    """📈 Statistiques d'utilisation des fonctionnalités premium"""
    try:
        subscription = await db.premium_subscriptions.find_one({
            "user_id": current_user['id'],
            "status": {"$in": ["active", "trialing"]}
        })
        
        if not subscription:
            raise HTTPException(
                status_code=403,
                detail="Accès réservé aux membres premium"
            )
        
        plan = PREMIUM_PLANS.get(subscription["plan_id"])
        if not plan:
            raise HTTPException(status_code=404, detail="Plan introuvable")
        
        # Calculer l'utilisation
        usage_stats = await _get_detailed_usage_stats(current_user['id'], plan)
        
        return {
            "subscription": {
                "plan": plan.name,
                "tier": plan.tier,
                "billing_period": subscription["billing_period"]
            },
            "current_period": {
                "start": subscription["current_period_start"],
                "end": subscription["current_period_end"]
            },
            "usage": usage_stats,
            "recommendations": _get_usage_recommendations(usage_stats, plan)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur stats usage premium: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des statistiques")

# ===============================================
# ENDPOINTS ADMIN
# ===============================================

@router.get("/admin/subscriptions")
async def get_all_premium_subscriptions(
    page: int = 1,
    limit: int = 50,
    admin_user: dict = Depends(get_admin_user)
):
    """👑 Liste tous les abonnements premium (admin)"""
    try:
        skip = (page - 1) * limit
        
        # Récupérer les abonnements avec pagination
        subscriptions = await db.premium_subscriptions.find(
            {},
            sort=[("created_at", -1)]
        ).skip(skip).limit(limit).to_list(None)
        
        # Enrichir avec les données utilisateur
        enriched_subscriptions = []
        for sub in subscriptions:
            user_data = await db.users.find_one({"id": sub["user_id"]})
            
            enriched_sub = {
                **sub,
                "user": {
                    "username": user_data.get("username", "Inconnu") if user_data else "Inconnu",
                    "email": user_data.get("email", "") if user_data else ""
                },
                "plan_name": PREMIUM_PLANS.get(sub["plan_id"], {}).get("name", "Plan inconnu")
            }
            enriched_subscriptions.append(enriched_sub)
        
        # Statistiques globales
        total_subscriptions = await db.premium_subscriptions.count_documents({})
        active_subscriptions = await db.premium_subscriptions.count_documents({"status": "active"})
        trial_subscriptions = await db.premium_subscriptions.count_documents({"status": "trialing"})
        
        # Revenus par plan
        revenue_by_plan = {}
        for plan_id, plan in PREMIUM_PLANS.items():
            monthly_subs = await db.premium_subscriptions.count_documents({
                "plan_id": plan_id,
                "billing_period": "monthly",
                "status": "active"
            })
            yearly_subs = await db.premium_subscriptions.count_documents({
                "plan_id": plan_id,
                "billing_period": "yearly", 
                "status": "active"
            })
            
            revenue_by_plan[plan_id] = {
                "monthly_revenue": monthly_subs * plan.price_monthly,
                "yearly_revenue": yearly_subs * plan.price_yearly,
                "total_subscribers": monthly_subs + yearly_subs
            }
        
        return {
            "subscriptions": enriched_subscriptions,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_subscriptions
            },
            "statistics": {
                "total_subscriptions": total_subscriptions,
                "active_subscriptions": active_subscriptions,
                "trial_subscriptions": trial_subscriptions,
                "revenue_by_plan": revenue_by_plan
            }
        }
        
    except Exception as e:
        app_logger.error(f"❌ Erreur admin subscriptions: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des abonnements")

# ===============================================
# FONCTIONS UTILITAIRES
# ===============================================

async def _get_or_create_stripe_customer(user: dict):
    """Récupère ou crée un customer Stripe"""
    try:
        # Chercher un customer existant
        existing_customer = await db.stripe_customers.find_one({"user_id": user['id']})
        
        if existing_customer:
            return stripe.Customer.retrieve(existing_customer['stripe_customer_id'])
        
        # Créer un nouveau customer
        customer = stripe.Customer.create(
            email=user.get('email', ''),
            name=user.get('username', ''),
            metadata={'user_id': user['id']}
        )
        
        # Sauvegarder en base
        await db.stripe_customers.insert_one({
            "user_id": user['id'],
            "stripe_customer_id": customer.id,
            "created_at": datetime.utcnow()
        })
        
        return customer
        
    except Exception as e:
        app_logger.error(f"❌ Erreur customer Stripe: {e}")
        raise

async def _activate_premium_features(user_id: str, plan_id: str):
    """Active les fonctionnalités premium pour un utilisateur"""
    try:
        plan = PREMIUM_PLANS.get(plan_id)
        if not plan:
            return
        
        # Mettre à jour le profil utilisateur
        await db.users.update_one(
            {"id": user_id},
            {
                "$set": {
                    "premium_tier": plan.tier,
                    "premium_activated_at": datetime.utcnow(),
                    "premium_features": {
                        "max_custom_themes": plan.max_custom_themes,
                        "analytics_retention_days": plan.analytics_retention_days,
                        "support_priority": plan.support_priority
                    }
                }
            }
        )
        
        # Attribuer les badges exclusifs
        from achievements import achievement_engine
        for badge_id in plan.exclusive_badges:
            await achievement_engine.award_badge_manually(user_id, badge_id, "premium_activation")
        
        app_logger.info(f"✅ Fonctionnalités premium activées: {user_id} -> {plan_id}")
        
    except Exception as e:
        app_logger.error(f"❌ Erreur activation premium: {e}")

async def _get_user_feature_usage(user_id: str, plan: PremiumPlan) -> Dict[str, int]:
    """Calcule l'utilisation des fonctionnalités par l'utilisateur"""
    try:
        usage = {}
        
        # Compter les thèmes personnalisés
        custom_themes = await db.user_custom_themes.count_documents({"user_id": user_id})
        usage["custom_themes"] = custom_themes
        
        return usage
        
    except Exception as e:
        app_logger.error(f"❌ Erreur calcul usage: {e}")
        return {}

async def _get_detailed_usage_stats(user_id: str, plan: PremiumPlan) -> Dict[str, Any]:
    """Statistiques détaillées d'utilisation"""
    # Implémentation complète selon les besoins
    return {
        "custom_themes": {"used": 0, "limit": plan.max_custom_themes},
        "analytics_queries": {"used": 0, "limit": 1000},
        "support_tickets": {"used": 0, "priority": plan.support_priority}
    }

def _get_usage_recommendations(usage_stats: Dict, plan: PremiumPlan) -> List[str]:
    """Recommandations basées sur l'utilisation"""
    recommendations = []
    
    themes_usage = usage_stats.get("custom_themes", {})
    if themes_usage.get("used", 0) >= themes_usage.get("limit", 0) * 0.8:
        recommendations.append("Vous approchez de votre limite de thèmes personnalisés")
    
    return recommendations

async def _schedule_premium_deactivation(user_id: str, deactivation_date: datetime):
    """Programme la désactivation des fonctionnalités premium"""
    # Dans une vraie implémentation, on utiliserait un système de tâches planifiées
    app_logger.info(f"📅 Désactivation premium programmée: {user_id} -> {deactivation_date}")

# Ajouter Stripe API key dans .env
async def setup_stripe_webhook():
    """Configure le webhook Stripe pour les événements d'abonnement"""
    # Dans une vraie implémentation, on configurerait les webhooks Stripe
    pass

app_logger.info("💰 Système Premium Elite chargé !")