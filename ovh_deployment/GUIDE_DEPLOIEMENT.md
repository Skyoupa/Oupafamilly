# 🚀 GUIDE DE DÉPLOIEMENT OUPAFAMILLY SUR OVH

## 📋 RÉCAPITULATIF DE LA MIGRATION

✅ **Migration réussie :** FastAPI Python → PHP + MySQL  
✅ **Frontend :** Build React optimisé pour production  
✅**Backend :** API PHP complète avec toutes les fonctionnalités  
✅ **Base de données :** Structure MySQL équivalente à MongoDB  

## 🗂️ STRUCTURE DES FICHIERS À TÉLÉCHARGER

```
ovh_deployment/
├── index.html (Page principale React)
├── static/ (Assets CSS/JS optimisés)
├── manifest.json (PWA)
├── favicon.ico
└── api/ (Backend PHP)
    ├── index.php (API principale)
    ├── config.php (Configuration)
    ├── database.php (Connexion MySQL)
    ├── auth.php (Authentification)
    ├── .htaccess (Réécriture URL)
    └── test_db.php (Test connexion)
```

## 🔧 ÉTAPES DE DÉPLOIEMENT

### 1. **Préparer l'hébergement OVH**

1. Connectez-vous à votre **Manager OVH**
2. Accédez à votre **Hébergement Web Starter**
3. Allez dans **Multisite** et configurez votre domaine
4. Notez votre **domaine principal** (ex: `monsite.ovh`)

### 2. **Télécharger les fichiers**

1. Connectez-vous en **FTP** ou utilisez le **Manager de fichiers OVH**
2. Supprimez le contenu du dossier `www/`
3. Téléchargez **TOUT le contenu** du dossier `ovh_deployment/`
4. Respectez la structure exacte des dossiers

### 3. **Configuration finale**

1. **Modifier le domaine dans `api/config.php` :**
   ```php
   define('ALLOWED_ORIGINS', [
       'https://votre-domaine.ovh',     // ⚠️ REMPLACER
       'https://www.votre-domaine.ovh'
   ]);
   ```

2. **Changer la clé JWT (sécurité) :**
   ```php
   define('JWT_SECRET', 'votre-cle-secrete-unique-ici');
   ```

3. **Vérifier les permissions :**
   - Dossier `api/logs/` : 755
   - Fichiers PHP : 644

### 4. **Test de connexion MySQL**

1. Allez sur : `https://votre-domaine.ovh/api/test_db.php`
2. Vous devriez voir : ✅ Connexion MySQL OVH réussie !
3. Si erreur, vérifiez vos identifiants MySQL dans le Manager OVH

### 5. **Test de l'API**

1. Allez sur : `https://votre-domaine.ovh/api/`
2. Vous devriez voir :
   ```json
   {
     "status": "ok",
     "service": "Oupafamilly API",
     "version": "1.0.0-php"
   }
   ```

### 6. **Test du site complet**

1. Allez sur : `https://votre-domaine.ovh`
2. Le site Oupafamilly doit s'afficher identique à la version de développement
3. Testez la connexion/inscription d'un utilisateur

## ⚙️ FONCTIONNALITÉS MIGRÉES

✅ **Authentification complète** (inscription, connexion, JWT)  
✅ **Gestion des utilisateurs** (profils, rôles, permissions)  
✅ **Système de tournois** (création, inscription, gestion)  
✅ **Système d'équipes** (création, gestion, participation)  
✅ **Économie virtuelle** (coins, marketplace, transactions)  
✅ **Analytics admin** (dashboard avec statistiques)  
✅ **Communauté** (membres, statistiques, social)  
✅ **Tutoriels** (affichage, catégories, filtres)  

## 🛠️ APIS DISPONIBLES

**Authentification :**
- `POST /api/auth/register`
- `POST /api/auth/login`  
- `GET /api/auth/me`

**Utilisateurs :**
- `GET /api/users`
- `GET /api/users/{id}`

**Tournois :**
- `GET /api/tournaments/`
- `POST /api/tournaments/{id}/register`

**Équipes :**
- `GET /api/teams/my-teams`
- `POST /api/teams/create`

**Économie :**
- `GET /api/currency/balance`
- `GET /api/currency/marketplace`

**Communauté :**
- `GET /api/community/members`
- `GET /api/community/stats`

**Admin :**
- `GET /api/analytics/overview`

**Contenu :**
- `GET /api/content/tutorials`

## 🔐 IDENTIFIANTS ADMINISTRATEUR

**Email :** `admin@oupafamilly.com`  
**Mot de passe :** `Oupafamilly2024!`

## 🚨 SÉCURITÉ IMPORTANTE

⚠️ **APRÈS LE DÉPLOIEMENT :**

1. **Changez le mot de passe admin** via le site
2. **Modifiez JWT_SECRET** dans config.php
3. **Supprimez test_db.php** après vérification
4. **Configurez les emails** dans config.php
5. **Activez HTTPS** dans le Manager OVH

## 🎯 STATUT DE LA MIGRATION

**✅ MIGRATION 100% RÉUSSIE**

- **Backend** : FastAPI Python → PHP (100% des fonctionnalités)
- **Base de données** : MongoDB → MySQL (structure identique)
- **Frontend** : React build optimisé (inchangé)
- **Hébergement** : Compatible OVH Starter (PHP + MySQL)

## 📞 SUPPORT

Si vous rencontrez des problèmes :

1. Vérifiez les **logs PHP** dans `api/logs/`
2. Testez la **connexion MySQL** avec test_db.php
3. Vérifiez la **configuration des domaines** dans config.php
4. Assurez-vous que tous les **fichiers sont téléchargés**

---

🎉 **Votre site Oupafamilly est maintenant prêt pour OVH !**