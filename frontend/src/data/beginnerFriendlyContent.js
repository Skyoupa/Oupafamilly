// Contenu spécialement conçu pour les débutants CS2
// Explications simples en français avec termes techniques du jeu en anglais

export const BEGINNER_FRIENDLY_CONTENT = {
  
  // ===== TUTORIELS DÉBUTANTS SIMPLIFIÉS (15) =====
  
  'interface-et-controles-de-base': {
    title: 'Interface et contrôles de base',
    level: 'Débutant',
    duration: '15 min',
    type: 'Fundamentals',
    image: 'https://images.unsplash.com/photo-1593280359364-5242f1958068?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzQwNjU1NHww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à utiliser les commandes de base dans Counter-Strike 2 avec des explications simples et claires.',
    objectives: [
      'Comprendre les touches de déplacement Z, Q, S, D',
      'Apprendre à viser avec la souris',
      'Connaître les touches importantes comme R (reload) et G (drop)',
      'Savoir utiliser TAB pour voir le scoreboard',
      'Comprendre comment acheter des armes avec B'
    ],
    content: `
# 🎮 Interface et Contrôles de Base CS2

## 🚀 Bienvenue dans Counter-Strike 2 !

Counter-Strike 2 est un jeu de tir où tu joues dans une équipe. Ne t'inquiète pas si ça semble compliqué au début - on va commencer par les bases !

## ⌨️ Les Touches les Plus Importantes

### 🏃 Se Déplacer
- **Z** = Avancer
- **Q** = Aller à gauche  
- **S** = Reculer
- **D** = Aller à droite
- **Shift** = Marcher sans bruit (très important !)
- **Ctrl** = S'accroupir

**Conseil de débutant** : Maintiens **Shift** quand tu veux être discret. Les ennemis peuvent t'entendre courir !

### 🔫 Utiliser les Armes
- **Clic gauche** = Tirer
- **Clic droit** = Viser (sur certaines armes)
- **R** = Recharger ton arme
- **G** = Lâcher ton arme au sol
- **1, 2, 3** = Changer d'arme rapidement

### 🛒 Acheter des Armes
- **B** = Ouvrir le menu d'achat
- **F1** à **F4** = Acheter rapidement (tu apprendras plus tard)
- **Échap** = Fermer le menu

**Important** : Tu peux acheter des armes seulement au début du round et dans ta base !

## 🖥️ Interface du Jeu

### 📊 Informations Importantes à l'Écran
- **En bas à droite** : Tes munitions (exemple : 30/120)
- **En haut** : Le temps restant du round
- **En haut à gauche** : Les scores des équipes
- **En bas à gauche** : Ta santé (max 100) et ton armor

### 🗺️ Le Radar (Mini-carte)
- **Point vert** = Toi
- **Points bleus** = Tes coéquipiers
- **Points rouges** = Ennemis repérés
- **Étoile** = Objectif à défendre ou attaquer

## 💰 L'Argent dans CS2

Tu gagnes de l'argent en :
- Tuant des ennemis
- Gagnant des rounds
- Plantant ou désamorçant la bombe

Tu dépenses de l'argent pour :
- Acheter des armes
- Acheter des grenades
- Acheter du gilet pare-balles (armor)

## 🎯 Conseils pour Bien Commencer

### ✅ Ce qu'il faut faire :
- **Écoute** : Utilise des écouteurs pour entendre les ennemis
- **Reste avec ton équipe** : Ne pars pas seul
- **Marche discrètement** avec **Shift** près des ennemis
- **Rechargez** après chaque combat avec **R**

### ❌ Ce qu'il ne faut pas faire :
- Ne cours pas partout - les ennemis t'entendent
- Ne gaspille pas tes munitions
- Ne quitte pas ton poste sans prévenir
- Ne rage pas si tu meurs - c'est normal au début !

## 🔧 Paramètres Recommandés pour Débutants

### 📱 Sensibilité de la Souris
- Commence avec une sensibilité moyenne
- Si tu vises trop vite → baisse la sensibilité
- Si tu vises trop lentement → augmente la sensibilité

### 🎵 Audio
- Active le son 3D pour entendre d'où viennent les ennemis
- Baisse la musique pour mieux entendre les pas
- Active les sous-titres si tu veux

## 🎮 Tes Premiers Pas

1. **Commence par un match contre bots** pour t'habituer
2. **Entraîne-toi à viser** dans le mode Practice
3. **Apprends une carte** comme Dust2 ou Mirage
4. **Joue avec des amis** c'est plus amusant !

## 💡 Astuce Spéciale Débutant

**TAB** = Affiche le tableau des scores
- Tu peux voir qui joue bien dans ton équipe
- Tu peux voir ton nombre de kills/deaths
- Tu peux voir le ping (connexion internet)

N'aie pas peur de mourir au début - même les professionnels ont commencé comme toi ! L'important c'est de s'amuser et d'apprendre petit à petit.

**Prochaine étape** : Une fois que tu maîtrises les contrôles, apprends l'économie (comment bien gérer ton argent) !
`,
    tips: [
      'Commence par jouer contre des bots pour t\'habituer sans stress',
      'Utilise des écouteurs - le son est très important dans CS2',
      'Marche avec Shift près des ennemis pour ne pas faire de bruit',
      'N\'aie pas peur de mourir au début, c\'est normal d\'apprendre',
      'Regarde des vidéos de joueurs pour comprendre les bases'
    ],
    links: [
      { name: '🎮 Mode Practice CS2', url: 'https://www.youtube.com/watch?v=practice-cs2' },
      { name: '⚙️ Paramètres recommandés', url: 'https://www.youtube.com/watch?v=settings-cs2' },
      { name: '🎧 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'economie-cs2-comprendre-les-achats': {
    title: 'Économie CS2 : comprendre les achats',
    level: 'Débutant',
    duration: '20 min',
    type: 'Economy',
    image: 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à gérer ton argent dans CS2 comme un pro. Découvre quand acheter, quand économiser et quelles armes choisir.',
    objectives: [
      'Comprendre comment gagner de l\'argent dans CS2',
      'Savoir quand acheter des armes et quand économiser',
      'Apprendre les prix des armes principales',
      'Comprendre l\'importance du armor et des grenades',
      'Savoir faire un "eco round" avec son équipe'
    ],
    content: `
# 💰 Économie CS2 : Comprendre les Achats

## 🤔 Pourquoi l'Argent est Important ?

Dans CS2, tu ne peux pas toujours acheter la meilleure arme. Tu dois **gérer ton argent** intelligemment pour aider ton équipe à gagner !

## 💵 Comment Gagner de l'Argent ?

### 🎯 Actions qui Rapportent :
- **Tuer un ennemi** = 300$ (varie selon l'arme)
- **Gagner un round** = 3250$ 
- **Perdre un round** = 1400$ → 1900$ → 2400$ → 2900$ (augmente à chaque défaite)
- **Planter la bombe** = 800$ (même si ton équipe perd)
- **Désamorcer la bombe** = 300$

### 💡 Astuce Débutant
Plus ton équipe perd de rounds d'affilée, plus vous gagnez d'argent ! C'est fait pour équilibrer le jeu.

## 🛒 Les Achats Essentiels

### 🔫 Armes Principales (Rifles)
- **AK-47** (T side) = 2700$ - Très puissante, tue en 1 coup à la tête
- **M4A4** (CT side) = 3100$ - Précise et stable
- **M4A1-S** (CT side) = 2900$ - Silencieuse, moins de munitions

### 🎯 Armes Secondaires
- **Glock-18** (T side) = Gratuite au début
- **USP-S** (CT side) = Gratuite au début
- **Desert Eagle** = 700$ - Très puissante mais difficile

### 🛡️ Protection
- **Armor** = 650$ - Réduit les dégâts de 50% !
- **Helmet** = 350$ en plus - Protège contre les headshots

**Important** : Achète toujours de l'armor avant une arme chère !

## 🎮 Stratégies d'Achat pour Débutants

### 💪 Full Buy (Achat Complet)
Quand tu as **4000$+** :
- Rifle (AK-47 ou M4)
- Armor + Helmet
- 1-2 grenades
- **Total** : ~4000-5000$

### 💰 Force Buy (Achat Forcé)
Quand tu as **2000-3000$** :
- Armor
- Arme moins chère (Galil, FAMAS)
- 1 grenade
- **Total** : ~2500-3000$

### 🚫 Eco Round (Économie)
Quand tu as **moins de 2000$** :
- Garde ton argent !
- Utilise le pistolet gratuit
- Achète éventuellement 1 grenade
- **But** : Économiser pour le round suivant

## 🕐 Quand Acheter ?

### ✅ Achète quand :
- Tu as assez d'argent pour rifle + armor
- C'est un round important (16-14 par exemple)
- Ton équipe fait un "full buy" ensemble

### ❌ N'achète pas quand :
- Tu n'as pas assez pour armor + arme décente
- Ton équipe fait "eco" (économie)
- C'est le dernier round du half

## 🎯 Conseils Pratiques

### 📊 Gestion d'Équipe
- **Regarde l'argent de tes coéquipiers** (TAB)
- **Communique** : "Je fais eco" ou "Je peux acheter"
- **Partagez** : Si tu as beaucoup d'argent, achète pour un ami

### 🎪 Rounds Spéciaux
- **Pistol Round** (1er round) : Armor + grenades
- **Anti-eco** : Ils n'ont pas d'argent → prends des armes proches
- **Eco vs Full Buy** : Ils sont riches → reste loin, utilise grenades

## 🔫 Prix des Armes Importantes

### 💥 Rifles
- AK-47 : 2700$
- M4A4 : 3100$
- M4A1-S : 2900$

### 🌪️ SMG (Mitraillettes)
- MP9 : 1250$
- UMP-45 : 1200$
- P90 : 2350$

### 💣 Grenades
- HE Grenade : 300$
- Flashbang : 200$
- Smoke : 300$
- Molotov/Incendiaire : 400$

## 🎮 Exemple Pratique

### Round 1 (Pistol Round)
- Tu commences avec 800$
- **Achète** : Armor (650$)
- **Reste** : 150$ → garde pour plus tard

### Round 2 (Si tu gagnes)
- Tu as ~3000$
- **Achète** : AK-47 (2700$) + HE grenade (300$)

### Round 3 (Si tu perds le round 2)
- Tu as ~1900$
- **Décision** : Eco round, garde ton argent !

## 💡 Erreurs de Débutant à Éviter

### ❌ Erreurs communes :
- Acheter une arme chère sans armor
- Acheter quand l'équipe fait eco
- Gaspiller l'argent sur des armes inutiles
- Ne pas regarder l'argent de l'équipe

### ✅ Bonnes habitudes :
- Toujours armor avant arme chère
- Communiquer avec l'équipe
- Garder de l'argent pour les rounds importants
- Apprendre les prix par cœur

## 🏆 Objectif Final

Maîtriser l'économie, c'est **50% de la victoire** dans CS2 ! Une équipe qui gère bien son argent gagne plus souvent.

**Prochaine étape** : Apprendre les mouvements de base pour survivre plus longtemps !
`,
    tips: [
      'Commence chaque round en regardant ton argent et celui de ton équipe',
      'Armor est plus important qu\'une arme chère - achète toujours l\'armor d\'abord',
      'Communique avec ton équipe : "eco" ou "full buy" ensemble',
      'Ne gaspille pas ton argent au round 15 - tu ne pourras plus acheter',
      'Apprends les prix par cœur pour prendre des décisions rapides'
    ],
    links: [
      { name: '💰 Calculateur économie CS2', url: 'https://www.csgoecon.com' },
      { name: '📊 Guide prix armes', url: 'https://www.youtube.com/watch?v=prices-cs2' },
      { name: '🎯 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'mouvement-et-deplacement-optimal': {
    title: 'Mouvement et déplacement optimal',
    level: 'Débutant',
    duration: '18 min',
    type: 'Movement',
    image: 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw1fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à te déplacer efficacement dans CS2. Découvre comment marcher silencieusement, comment sauter et comment éviter les balles.',
    objectives: [
      'Maîtriser les déplacements silencieux avec Shift',
      'Apprendre à utiliser Ctrl pour s\'accroupir',
      'Comprendre l\'importance du sound dans CS2',
      'Savoir quand courir et quand marcher',
      'Apprendre les bases du bunny hop'
    ],
    content: `
# 🏃 Mouvement et Déplacement Optimal

## 🎯 Pourquoi le Mouvement est Important ?

Dans CS2, **bien se déplacer peut sauver ta vie** ! Les ennemis t'entendent, te voient et peuvent prédire où tu vas. Apprends à bouger intelligemment !

## 🔇 Les Différents Types de Déplacement

### 🏃 Running (Course normale)
- **Touches** : Z, Q, S, D (sans Shift)
- **Vitesse** : Rapide
- **Bruit** : TRÈS FORT - tous les ennemis t'entendent
- **Quand utiliser** : Quand tu es loin des ennemis

### 🚶 Walking (Marche silencieuse)
- **Touches** : Z, Q, S, D + **Shift maintenu**
- **Vitesse** : Lente
- **Bruit** : Silencieux
- **Quand utiliser** : Près des ennemis ou dans des zones dangereuses

### 🦆 Crouching (Accroupi)
- **Touche** : **Ctrl**
- **Vitesse** : Très lente
- **Bruit** : Silencieux
- **Bonus** : Plus précis pour tirer

## 🎵 L'Importance du Son

### 👂 Ce que les Ennemis Entendent :
- **Pas de course** = Audible à 20 mètres
- **Pas de marche** = Audible à 5 mètres seulement
- **Atterrissage de saut** = Très audible
- **Recharge d'arme** = Audible

### 🔇 Astuces pour Être Discret :
- **Shift** quand tu approches des angles
- **Ctrl** quand tu veux viser précisément
- **Marche** dans les zones communes (mid, long, etc.)
- **Arrête-toi** pour écouter les ennemis

## 🎮 Techniques de Déplacement

### 🏃 Strafe Running (Course latérale)
- **Utilise** : Q et D avec la souris
- **Pourquoi** : Plus difficile à toucher
- **Technique** : Cours en zigzag, pas en ligne droite

### 🦆 Crouch Peeking (Espionnage accroupi)
- **Technique** : Ctrl + Q/D pour regarder un angle
- **Avantage** : Tête plus basse, plus difficile à headshot
- **Inconvénient** : Plus lent à fuir

### 🎯 Jiggle Peeking (Espionnage rapide)
- **Technique** : Q/D rapidement pour voir sans être vu
- **But** : Récupérer des informations sans risquer sa vie
- **Timing** : Très rapide, juste pour voir

## 🚪 Franchir les Angles

### ✅ Bonne Méthode :
1. **Approche** en marchant (Shift)
2. **Écoute** s'il y a des ennemis
3. **Dégaine** ton arme
4. **Peek** (regarde) l'angle rapidement
5. **Tire** ou **recule** selon la situation

### ❌ Mauvaise Méthode :
- Courir directement dans l'angle
- Ne pas écouter avant
- Regarder l'angle trop lentement
- Rester exposé trop longtemps

## 🎪 Mouvements Avancés pour Débutants

### 🐰 Bunny Hop (Saut enchaîné)
- **Technique** : Espace + Q/D + mouvement souris
- **Difficulté** : Difficile à maîtriser
- **Conseil** : Commence par des sauts simples

### 🏃 Counter-Strafing (Arrêt net)
- **Technique** : Si tu vas à droite (D), appuie sur Q pour t'arrêter net
- **Pourquoi** : Stopper ton élan pour tirer précisément
- **Exemple** : D → Q (arrêt) → Tirer

### 🎯 Shoulder Peeking (Montrer l'épaule)
- **Technique** : Montre juste ton épaule pour faire tirer l'ennemi
- **But** : Il gaspille ses balles, tu sais où il est
- **Timing** : Très rapide, juste l'épaule

## 🗺️ Déplacement selon les Cartes

### 🏜️ Dust2 (Exemple)
- **Long A** : Marche obligatoire (snipers)
- **Tunnels** : Cours, les distances sont courtes
- **Mid** : Marche, zone très surveillée
- **Site A** : Crouch derrière les caisses

### 🎯 Conseils Généraux :
- **Zones ouvertes** : Marche pour éviter les snipers
- **Zones fermées** : Cours, mais écoute aux angles
- **Sites** : Marche, c'est là que les ennemis t'attendent

## 🛡️ Survivre aux Combats

### 🏃 Éviter les Balles :
- **Strafe** (Q/D) pendant les combats
- **Crouch** au bon moment (pas toujours)
- **Utilise les murs** pour te couvrir
- **Recule** si tu perds le combat

### 🎯 Positionnement :
- **Ne reste jamais** au même endroit
- **Change d'angle** après un kill
- **Utilise les obstacles** (caisses, murs)
- **Garde toujours** une sortie de secours

## 🎮 Entraînement Pratique

### 📚 Exercices Simples :
1. **Marche silencieuse** : Traverse une carte entière en shift
2. **Jiggle peek** : Entraîne-toi sur des angles
3. **Counter-strafe** : Cours et arrête-toi net
4. **Bunny hop** : Commence par 2-3 sauts enchaînés

### 🎯 Maps d'Entraînement :
- **aim_botz** : Pour pratiquer les mouvements
- **yprac_maps** : Pour apprendre les angles
- **kz_maps** : Pour les mouvements avancés

## 💡 Erreurs de Débutant

### ❌ Erreurs communes :
- Courir partout sans réfléchir
- Ne pas utiliser Shift près des ennemis
- Rester immobile pendant les combats
- Ne pas écouter les bruits de pas

### ✅ Bonnes habitudes :
- Shift dès que tu entends des ennemis
- Bouge pendant les combats
- Écoute plus que tu ne regardes
- Change de position après chaque kill

## 🏆 Objectif Final

Maîtriser les déplacements te rendra **50% plus difficile à tuer** ! Les ennemis auront du mal à te prédire et à t'entendre arriver.

**Prochaine étape** : Apprendre à bien viser avec le crosshair !
`,
    tips: [
      'Shift est ton meilleur ami - utilise-le dès que tu entends des ennemis',
      'Bouge pendant les combats, ne reste jamais immobile',
      'Écoute les bruits de pas - ils te donnent plus d\'infos que la vue',
      'Change de position après chaque kill pour surprendre',
      'Entraîne-toi sur des maps de movement pour progresser'
    ],
    links: [
      { name: '🏃 Maps d\'entraînement movement', url: 'https://steamcommunity.com/workshop/browse/?appid=730&searchtext=movement' },
      { name: '🎯 Guide bunny hop débutant', url: 'https://www.youtube.com/watch?v=bhop-beginner' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'visee-et-reglages-crosshair': {
    title: 'Visée et réglages crosshair',
    level: 'Débutant',
    duration: '25 min',
    type: 'Aiming',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à bien viser dans CS2. Découvre comment régler ton crosshair, améliorer ta précision et comprendre le recul des armes.',
    objectives: [
      'Comprendre l\'importance du crosshair dans CS2',
      'Apprendre à régler ton crosshair selon tes préférences',
      'Maîtriser les bases du crosshair placement',
      'Comprendre le recul des armes (spray pattern)',
      'Améliorer ta précision avec des exercices pratiques'
    ],
    content: `
# 🎯 Visée et Réglages Crosshair

## 🎮 Qu'est-ce que le Crosshair ?

Le **crosshair** (réticule) est la petite croix au centre de ton écran. C'est **l'outil le plus important** pour viser dans CS2 !

## ⚙️ Réglages Crosshair pour Débutants

### 🎨 Crosshair Recommandé pour Commencer :
\`\`\`
cl_crosshairsize 2
cl_crosshairthickness 1
cl_crosshairgap 0
cl_crosshairdot 0
cl_crosshair_drawoutline 1
cl_crosshair_outlinethickness 1
cl_crosshaircolor 4 // cyan/bleu
\`\`\`

### 🎯 Comment Changer ton Crosshair :
1. **Ouvre la console** (touche ²)
2. **Tape les commandes** une par une
3. **Ou utilise** le menu Settings → Game Settings → Crosshair

### 🌈 Couleurs Populaires :
- **Vert** (1) : Facile à voir sur toutes les cartes
- **Jaune** (2) : Très visible
- **Bleu** (4) : Moins fatigant pour les yeux
- **Cyan** (4) : Populaire chez les pros

## 🎯 Crosshair Placement (Placement du Réticule)

### 📍 Règle d'Or :
**Garde toujours ton crosshair à hauteur de tête** ! C'est la technique la plus importante.

### ✅ Bon Placement :
- **Hauteur** : Niveau de la tête des ennemis
- **Position** : Près des angles où ils peuvent apparaître
- **Anticipation** : Là où l'ennemi va être, pas où il est

### ❌ Mauvais Placement :
- Crosshair pointé vers le sol
- Trop haut (au-dessus des têtes)
- Au centre de l'écran sans réfléchir
- Loin des angles importants

## 🎮 Techniques de Visée

### 🎯 Pre-aiming (Pré-visée)
- **Technique** : Viser où l'ennemi va apparaître AVANT qu'il apparaisse
- **Avantage** : Tu tires plus vite
- **Pratique** : Apprendre les angles communs de chaque carte

### 🎪 Flicking (Mouvement rapide)
- **Technique** : Mouvement rapide du crosshair vers l'ennemi
- **Quand** : Quand l'ennemi apparaît où tu ne l'attendais pas
- **Entraînement** : Pratique sur aim_botz

### 🎯 Tracking (Suivi)
- **Technique** : Suivre l'ennemi qui bouge avec ton crosshair
- **Difficulté** : Difficile, demande de l'entraînement
- **Conseil** : Prédis où il va, ne suis pas où il est

## 🔫 Comprendre le Recul (Spray Pattern)

### 🎪 Qu'est-ce que le Recul ?
Quand tu tires plusieurs balles, **l'arme monte et bouge** ! Les balles ne vont pas où tu vises.

### 🎯 Recul de l'AK-47 :
1. **Premières balles** : Montent droit
2. **Milieu** : Vont à gauche
3. **Fin** : Vont à droite
4. **Solution** : Bouge ta souris dans le sens opposé

### 🎮 Conseils pour Débutants :
- **Tire par rafales** de 3-5 balles maximum
- **Arrête de tirer** si tu rates
- **Recommence** ta visée
- **N'essaie pas** de contrôler 30 balles au début

## 🎯 Entraînement de la Visée

### 🎮 Maps d'Entraînement :
- **aim_botz** : Bots immobiles pour pratiquer
- **aim_redline** : Cibles qui bougent
- **training_aim_csgo2** : Exercices variés

### 📚 Routine d'Entraînement (15 minutes) :
1. **5 minutes** : Crosshair placement sur aim_botz
2. **5 minutes** : Flicking sur des cibles rapides
3. **5 minutes** : Spray control sur un mur

### 🎯 Objectifs d'Entraînement :
- **Headshots** : Vise toujours la tête
- **Régularité** : Mieux vaut 10 minutes par jour que 2h une fois
- **Patience** : La précision vient avec le temps

## 🖱️ Paramètres Souris

### ⚙️ Sensibilité Recommandée :
- **Débutant** : 2.0 - 3.0 (in-game)
- **DPI** : 800-1600
- **Formule** : DPI × Sensibilité = 1600-2400

### 🎯 Comment Trouver ta Sensibilité :
1. **Teste** différentes valeurs
2. **Trop rapide** ? Baisse la sensibilité
3. **Trop lent** ? Augmente la sensibilité
4. **Garde** la même sensibilité une fois trouvée !

### 🖱️ Conseils Souris :
- **Désactive** l'accélération souris
- **Utilise** un grand tapis de souris
- **Nettoie** régulièrement ta souris
- **Tiens** ta souris avec toute ta main

## 🎮 Visée selon les Situations

### 🏃 Ennemi qui Bouge :
- **Prédis** sa direction
- **Vise** où il va être
- **Tire** au bon moment
- **Suis** son mouvement

### 🎯 Ennemi Immobile :
- **Prends ton temps** pour viser
- **Vise la tête** pour un headshot
- **Tire** une balle précise
- **Ajuste** si tu rates

### 🎪 Combat Rapproché :
- **Vise large** (le corps)
- **Tire rapidement**
- **Bouge** pendant le combat
- **Priorise** la vitesse sur la précision

## 💡 Erreurs de Débutant

### ❌ Erreurs communes :
- Crosshair pointé vers le sol
- Changer de sensibilité trop souvent
- Tirer trop de balles d'affilée
- Ne pas s'entraîner régulièrement

### ✅ Bonnes habitudes :
- Crosshair toujours à hauteur de tête
- Sensibilité constante
- Rafales courtes (3-5 balles)
- Entraînement quotidien

## 🏆 Objectif Final

Une **bonne visée** te permettra de gagner 70% de tes duels ! C'est la base de tout bon joueur CS2.

**Prochaine étape** : Apprendre les différentes armes et leurs particularités !
`,
    tips: [
      'Garde toujours ton crosshair à hauteur de tête - c\'est la règle d\'or',
      'Trouve ta sensibilité idéale et ne la change plus jamais',
      'Entraîne-toi 10 minutes par jour plutôt que 2h une fois par semaine',
      'Tire par rafales de 3-5 balles maximum au début',
      'Utilise un crosshair bien visible - vert ou cyan sont parfaits'
    ],
    links: [
      { name: '🎯 Générateur de crosshair', url: 'https://www.crashz.net/crosshair-generator' },
      { name: '🎮 aim_botz workshop', url: 'https://steamcommunity.com/sharedfiles/filedetails/?id=243702660' },
      { name: '📊 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'presentation-des-armes-principales': {
    title: 'Présentation des armes principales',
    level: 'Débutant',
    duration: '22 min',
    type: 'Weapons',
    image: 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Découvre les armes principales de CS2. Apprends leurs forces, faiblesses et quand les utiliser pour dominer tes adversaires.',
    objectives: [
      'Connaître les armes principales (rifles, pistols, SMG)',
      'Comprendre les différences entre armes T et CT',
      'Apprendre les prix et situations d\'utilisation',
      'Maîtriser les armes essentielles pour débuter',
      'Savoir choisir la bonne arme selon ton budget'
    ],
    content: `
# 🔫 Présentation des Armes Principales

## 🎯 Pourquoi Connaître les Armes ?

Dans CS2, **chaque arme a ses forces et faiblesses**. Connaître les armes te permet de :
- Choisir la bonne arme selon ton budget
- Comprendre les forces de tes ennemis
- Adapter ton style de jeu
- Maximiser tes chances de victoire

## 🎮 Catégories d'Armes

### 🔫 Rifles (Fusils d'Assaut)
- **Dégâts** : Élevés
- **Précision** : Très bonne
- **Prix** : Cher (2700-3100$)
- **Utilisation** : Combats moyens/longs

### 🎯 Pistols (Pistolets)
- **Dégâts** : Moyens
- **Précision** : Bonne
- **Prix** : Pas cher (0-700$)
- **Utilisation** : Combats proches, eco rounds

### 🌪️ SMG (Mitraillettes)
- **Dégâts** : Moyens
- **Précision** : Moyenne
- **Prix** : Moyen (1200-2350$)
- **Utilisation** : Combats proches, anti-eco

### 🎯 Sniper Rifles (Fusils de Précision)
- **Dégâts** : Très élevés
- **Précision** : Excellente
- **Prix** : Très cher (4750$)
- **Utilisation** : Combats longs, AWP

## 🔫 Rifles - Les Armes Principales

### 🔥 AK-47 (Terrorist side)
- **Prix** : 2700$
- **Dégâts** : 36 (tête: 143)
- **Cadence** : 600 coups/min
- **Portée** : Excellente

**Avantages** :
- Tue en 1 headshot même avec casque
- Très puissante à toutes distances
- Bon rapport qualité/prix

**Inconvénients** :
- Recul difficile à contrôler
- Pas de mode rafale
- Bruyante

**Quand l'utiliser** : Combats longs, quand tu as 2700$+

### 🎯 M4A4 (Counter-Terrorist side)
- **Prix** : 3100$
- **Dégâts** : 33 (tête: 131)
- **Cadence** : 666 coups/min
- **Portée** : Excellente

**Avantages** :
- Très précise
- Recul plus facile que l'AK
- 30 balles par chargeur

**Inconvénients** :
- Ne tue pas en 1 headshot avec casque
- Plus chère que l'AK
- Dégâts moindres

**Quand l'utiliser** : Défense, combats moyens/longs

### 🔇 M4A1-S (Counter-Terrorist side)
- **Prix** : 2900$
- **Dégâts** : 38 (tête: 151)
- **Cadence** : 600 coups/min
- **Portée** : Excellente

**Avantages** :
- Silencieuse (pas de flash)
- Très précise
- Moins chère que M4A4

**Inconvénients** :
- Seulement 20 balles par chargeur
- Cadence plus lente
- Moins de munitions de réserve

**Quand l'utiliser** : Positions cachées, combats précis

## 🎯 Pistols - Armes Secondaires

### 🔫 Glock-18 (Terrorist - Gratuit)
- **Prix** : 0$ (arme de départ)
- **Dégâts** : 28 (tête: 111)
- **Cadence** : 400 coups/min
- **Spécial** : Mode rafale (clic droit)

**Conseil débutant** : Utilise le mode rafale en combat rapproché !

### 🎯 USP-S (Counter-Terrorist - Gratuit)
- **Prix** : 0$ (arme de départ)
- **Dégâts** : 35 (tête: 139)
- **Cadence** : 352 coups/min
- **Spécial** : Silencieuse

**Conseil débutant** : Plus précise que le Glock, prends ton temps pour viser !

### 💥 Desert Eagle (Les deux équipes)
- **Prix** : 700$
- **Dégâts** : 63 (tête: 249)
- **Cadence** : 267 coups/min
- **Spécial** : Tue en 1 headshot

**Avantages** :
- Dégâts énormes
- Tue en 1 headshot même avec casque
- Portée excellente

**Inconvénients** :
- Très difficile à maîtriser
- Recul énorme
- Seulement 7 balles

**Conseil débutant** : Difficile pour débuter, mais très puissante !

## 🌪️ SMG - Mitraillettes

### 🎮 MP9 (Counter-Terrorist)
- **Prix** : 1250$
- **Dégâts** : 26 (tête: 101)
- **Cadence** : 857 coups/min
- **Utilisation** : Anti-eco, combat rapproché

### 🔫 MAC-10 (Terrorist)
- **Prix** : 1050$
- **Dégâts** : 29 (tête: 116)
- **Cadence** : 800 coups/min
- **Utilisation** : Rush, combat rapproché

### 🎯 UMP-45 (Les deux équipes)
- **Prix** : 1200$
- **Dégâts** : 35 (tête: 138)
- **Cadence** : 666 coups/min
- **Utilisation** : Anti-eco, bon compromis

**Conseil débutant** : Excellente arme pour les rounds où tu n'as pas assez pour un rifle !

## 🎯 Conseils pour Choisir son Arme

### 💰 Selon ton Budget :
- **0-800$** : Pistolet de base + armor
- **1200-2000$** : UMP-45 ou MP9/MAC-10
- **2700-3100$** : AK-47 ou M4
- **4750$** : AWP (si tu sais viser)

### 🗺️ Selon la Carte :
- **Cartes ouvertes** (Dust2) : Rifles, AWP
- **Cartes fermées** (Inferno) : SMG, pistols
- **Cartes mixtes** (Mirage) : Toutes les armes

### 🎮 Selon ton Rôle :
- **Entry fragger** : AK-47, MAC-10
- **Support** : M4A1-S, UMP-45
- **AWPer** : AWP, Desert Eagle
- **Lurker** : M4A1-S, USP-S

## 🎯 Armes Recommandées pour Débuter

### 🌟 Top 5 Armes Faciles :
1. **UMP-45** : Facile à utiliser, pas chère
2. **M4A4** : Précise, recul gérable
3. **AK-47** : Puissante, standard
4. **USP-S** : Précise, silencieuse
5. **MP9** : Rapide, anti-eco

### 🎮 Plan d'Apprentissage :
1. **Semaine 1** : Maîtrise les pistolets de base
2. **Semaine 2** : Apprends l'UMP-45
3. **Semaine 3** : Commence l'AK-47
4. **Semaine 4** : Essaie l'AWP avec précaution

## 💡 Erreurs de Débutant

### ❌ Erreurs communes :
- Acheter des armes trop chères pour son niveau
- Utiliser l'AWP sans savoir viser
- Changer d'arme trop souvent
- Ignorer les armes "moins prestigieuses"

### ✅ Bonnes habitudes :
- Commence par les armes faciles
- Maîtrise une arme avant d'en apprendre une autre
- Achète selon ton budget
- Adapte ton arme à la situation

## 🏆 Objectif Final

Connaître les armes te permet de faire les **bons choix stratégiques** et d'optimiser tes chances de victoire selon chaque situation !

**Prochaine étape** : Apprendre les cartes populaires comme Dust2 !
`,
    tips: [
      'Commence par maîtriser l\'UMP-45 - excellente arme pour débuter',
      'Apprends l\'AK-47 progressivement - c\'est l\'arme la plus importante',
      'Ne néglige pas les pistolets - ils peuvent sauver des rounds',
      'Achète selon ton budget, pas selon tes envies',
      'Entraîne-toi avec une arme à la fois pour bien la maîtriser'
    ],
    links: [
      { name: '🔫 Stats détaillées des armes', url: 'https://www.csgostats.gg/weapons' },
      { name: '🎯 Maps d\'entraînement armes', url: 'https://steamcommunity.com/workshop/browse/?appid=730&searchtext=weapon' },
      { name: '📊 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'maps-active-duty-dust2-basics': {
    title: 'Maps Active Duty : Dust2 basics',
    level: 'Débutant',
    duration: '20 min',
    type: 'Maps',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Apprends les bases de Dust2, la carte la plus populaire de CS2. Découvre les positions importantes et les stratégies simples.',
    objectives: [
      'Connaître les noms des zones importantes (Long A, Short A, Mid, etc.)',
      'Comprendre les positions de base sur Dust2',
      'Apprendre les routes principales pour attaquer',
      'Savoir défendre les sites A et B efficacement',
      'Comprendre l\'importance du contrôle de Mid'
    ],
    content: `
# 🗺️ Dust2 Basics - Les Bases

## 🎯 Pourquoi Dust2 ?

Dust2 est la carte **la plus populaire** de CS2 ! Elle est simple à comprendre, parfaite pour débuter et très équilibrée.

## 🗺️ Plan de Dust2

### 🎮 Zones Principales :
- **Long A** : Couloir long vers le site A
- **Short A** (Cat) : Chemin court vers le site A  
- **Mid** : Centre de la carte
- **Tunnels** : Passage vers le site B
- **Site A** : Objectif A à défendre/attaquer
- **Site B** : Objectif B à défendre/attaquer

### 🎯 Spawn Points :
- **Terrorists** : Spawn près des tunnels
- **Counter-Terrorists** : Spawn près des sites

## 🎮 Côté Terrorist (Attaquants)

### 🎯 Stratégies Simples :
1. **Rush B** : Tous les 5 joueurs foncent vers B par les tunnels
2. **Split A** : 3 joueurs Long A + 2 joueurs Short A
3. **Mid Control** : Contrôler Mid puis aider Long A
4. **Fake A, Go B** : Faire du bruit sur A, puis aller B

### 🗺️ Positions Importantes T :
- **T Spawn** : Où tu commences
- **Tunnels** : Chemin vers B
- **Mid** : Centre stratégique
- **Long A** : Couloir vers A
- **Short A** : Escaliers vers A

## 🛡️ Côté Counter-Terrorist (Défenseurs)

### 🎯 Positions de Base :
- **1 joueur Long A** : Défend le long couloir
- **1 joueur Short A** : Défend les escaliers
- **1 joueur Mid** : Contrôle le centre
- **2 joueurs B** : Défendent le site B

### 🎮 Rotations :
- **De A vers B** : Passe par Mid ou CT Spawn
- **De B vers A** : Passe par CT Spawn
- **Support Mid** : Aide Long A ou Short A

## 🎯 Positions Détaillées

### 🏜️ Long A (Couloir Long)
**Terrorists** :
- **T Spawn** → **Long Doors** → **Long A** → **Site A**
- **Conseils** : Marche avec Shift, attention aux snipers

**Counter-Terrorists** :
- **Position** : Derrière les caisses ou dans le coin
- **Conseils** : Utilise l'AWP si tu sais viser

### 🏃 Short A (Catwalk)
**Terrorists** :
- **T Spawn** → **Mid** → **Short A** → **Site A**
- **Conseils** : Attention aux grenades des CT

**Counter-Terrorists** :
- **Position** : Sur la plateforme ou derrière les caisses
- **Conseils** : Utilise les flashbangs

### 🎯 Mid (Centre)
**Terrorists** :
- **Contrôle** : Essentiel pour aider Long A
- **Positions** : Derrière les caisses ou sur Xbox

**Counter-Terrorists** :
- **Position** : Près des portes ou sur la plateforme
- **Conseils** : Smoke pour bloquer la vue

### 🚇 Tunnels vers B
**Terrorists** :
- **Chemin** : **T Spawn** → **Tunnels** → **Site B**
- **Conseils** : Attention aux bombes et aux smokes

**Counter-Terrorists** :
- **Position** : Dans le site B ou à l'entrée des tunnels
- **Conseils** : Utilise les grenades pour retarder

## 🎮 Conseils pour Débutants

### ✅ Bonnes Pratiques :
- **Communique** : Dis où tu vois les ennemis
- **Reste avec ton équipe** : Ne pars pas seul
- **Utilise les smokes** : Bloque la vue des snipers
- **Écoute** : Les bruits de pas donnent des infos

### ❌ Erreurs Communes :
- Courir dans Long A sans regarder
- Rester seul sur Short A
- Ignorer Mid
- Ne pas communiquer avec l'équipe

## 🎯 Stratégies Spécifiques

### 🏃 Rush B (Facile)
**Plan** : Tous les 5 T vont vers B
**Execution** :
1. **Achetez** : Armor + SMG/rifles
2. **Coordonnez** : Partez tous ensemble
3. **Spammez** : Tirez à travers les smokes
4. **Plantez** : Vite la bombe sur B

### 🎯 Split A (Intermédiaire)
**Plan** : 3 Long A + 2 Short A
**Execution** :
1. **Long A** : Avance doucement
2. **Short A** : Attend le signal
3. **Attaque** : Simultanément des deux côtés
4. **Trade** : Aide ton coéquipier si il meurt

### 🎮 Mid Control (Avancé)
**Plan** : Contrôler Mid puis aider
**Execution** :
1. **Smoke Mid** : Bloque la vue CT
2. **Prends Xbox** : Position importante
3. **Aide Long A** : Tire dans le dos des CT
4. **Rotate** : Va aider Short A si besoin

## 🗺️ Callouts Importants

### 🎯 Noms des Positions :
- **Long A** : Le long couloir
- **Short A** / **Cat** : Les escaliers
- **Mid** : Le centre
- **Xbox** : Les caisses au milieu
- **Tunnels** : Passage vers B
- **Site A** : Objectif A
- **Site B** : Objectif B
- **CT Spawn** : Spawn des CT

### 💬 Exemples de Communication :
- "Ennemi Long A !"
- "Ils rushent B !"
- "AWP Mid, attention !"
- "Site A libre, venez !"

## 🏆 Objectif Final

Maîtriser Dust2 te donne une **base solide** pour comprendre CS2. C'est la carte parfaite pour apprendre les stratégies de base !

**Prochaine étape** : Apprendre Mirage, une autre carte populaire !
`,
    tips: [
      'Commence par apprendre les noms des zones - c\'est essentiel pour communiquer',
      'En T, ne va jamais seul Long A - c\'est très dangereux',
      'En CT, contrôle Mid pour aider tes coéquipiers sur A',
      'Utilise des smokes pour bloquer la vue des snipers',
      'Écoute les bruits de pas pour deviner où vont les ennemis'
    ],
    links: [
      { name: '🗺️ Dust2 callouts interactive', url: 'https://www.simpleradar.com/dust2' },
      { name: '📹 Dust2 walkthrough débutant', url: 'https://www.youtube.com/watch?v=dust2-beginner' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'maps-active-duty-mirage-basics': {
    title: 'Maps Active Duty : Mirage basics',
    level: 'Débutant',
    duration: '20 min',
    type: 'Maps',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Découvre Mirage, une carte équilibrée et populaire. Apprends les routes principales et les stratégies de base.',
    objectives: [
      'Connaître les zones importantes (A Site, B Site, Mid, Connector)',
      'Comprendre les routes d\'attaque et de défense',
      'Apprendre les positions de base sur Mirage',
      'Maîtriser les stratégies simples d\'équipe',
      'Comprendre l\'importance du contrôle Mid'
    ],
    content: `
# 🗺️ Mirage Basics - Les Bases

## 🎯 Pourquoi Mirage ?

Mirage est une carte **très équilibrée** entre Terrorists et Counter-Terrorists. Elle est excellente pour apprendre les stratégies d'équipe !

## 🗺️ Plan de Mirage

### 🎮 Zones Principales :
- **A Site** : Objectif A avec les caisses
- **B Site** : Objectif B avec les appartements
- **Mid** : Centre de la carte
- **Connector** : Lien entre Mid et A
- **Ramp** : Montée vers A
- **Apartments** : Appartements vers B

### 🎯 Particularités :
- **Carte fermée** : Beaucoup de coins et d'angles
- **Équilibrée** : Pas d'avantage net pour une équipe
- **Stratégique** : Beaucoup de possibilités tactiques

## 🎮 Côté Terrorist (Attaquants)

### 🎯 Stratégies Simples :
1. **Rush B Apps** : Tous vers B par les appartements
2. **A Site Execute** : Attaque coordonnée sur A
3. **Mid Control** : Contrôler Mid puis Connector
4. **Split B** : Apps + Mid vers B

### 🗺️ Routes d'Attaque :
- **Vers A** : T Spawn → Mid → Connector → A Site
- **Vers A** : T Spawn → Ramp → A Site
- **Vers B** : T Spawn → Apartments → B Site
- **Vers B** : T Spawn → Mid → Underpass → B Site

## 🛡️ Côté Counter-Terrorist (Défenseurs)

### 🎯 Setup Standard :
- **2 joueurs A** : 1 Site A + 1 Connector
- **2 joueurs B** : 1 Site B + 1 Apps
- **1 joueur Mid** : Contrôle le centre

### 🎮 Rotations :
- **De A vers B** : Passe par Connector et Mid
- **De B vers A** : Passe par Underpass et Mid
- **Support Mid** : Aide selon les besoins

## 🎯 Positions Détaillées

### 🏠 A Site
**Terrorists** :
- **Ramp** : Montée directe vers A
- **Connector** : Passage depuis Mid
- **Conseils** : Utilise les smokes et flashbangs

**Counter-Terrorists** :
- **Site** : Derrière les caisses ou dans les coins
- **Connector** : Contrôle le passage depuis Mid
- **Conseils** : Communique avec Mid

### 🏢 B Site (Apartments)
**Terrorists** :
- **Apps** : Appartements vers B
- **Underpass** : Passage depuis Mid
- **Conseils** : Attention aux CT qui peuvent être partout

**Counter-Terrorists** :
- **Site B** : Défend le site depuis différents angles
- **Apps** : Contrôle les appartements
- **Conseils** : Utilise les grenades pour retarder

### 🎯 Mid (Centre)
**Terrorists** :
- **Mid** : Contrôle essentiel pour les rotations
- **Top Mid** : Position élevée
- **Conseils** : Smoke pour bloquer les snipers

**Counter-Terrorists** :
- **Mid** : Position centrale pour aider A et B
- **Connector** : Lien vers A Site
- **Conseils** : Très importante pour les rotations

## 🎮 Conseils pour Débutants

### ✅ Bonnes Pratiques :
- **Smoke Mid** : Bloque la vue des snipers CT
- **Clear angles** : Regarde chaque coin avant d'avancer
- **Communique** : Dis où tu vois les ennemis
- **Utilisez les grenades** : Très importantes sur Mirage

### ❌ Erreurs Communes :
- Courir dans Apps sans regarder
- Ignorer Mid
- Ne pas utiliser de smokes
- Mauvaise communication

## 🎯 Stratégies Spécifiques

### 🏃 Rush B Apps (Facile)
**Plan** : Tous les 5 T vont vers B
**Execution** :
1. **Achetez** : Armor + SMG/rifles + grenades
2. **Smoke** : Bloc la vue depuis Mid
3. **Rush** : Tous ensemble dans Apps
4. **Clear** : Vérifiez chaque angle
5. **Plant** : Vite la bombe sur B

### 🎯 A Site Execute (Intermédiaire)
**Plan** : Attaque coordonnée sur A
**Execution** :
1. **Setup** : 3 joueurs Ramp + 2 joueurs Connector
2. **Smokes** : Bloquez CT et Jungle
3. **Flash** : Aveuglent les défenseurs
4. **Execute** : Attaque simultanée
5. **Trade** : Aide tes coéquipiers

### 🎮 Mid Control (Avancé)
**Plan** : Contrôler Mid puis aider
**Execution** :
1. **Smoke Mid** : Bloque la vue CT
2. **Prends Top Mid** : Position importante
3. **Connector** : Aide l'attaque sur A
4. **Underpass** : Ou aide l'attaque sur B

## 🗺️ Callouts Importants

### 🎯 Noms des Positions :
- **A Site** : Le site A
- **B Site** : Le site B  
- **Mid** : Le centre
- **Connector** : Lien Mid-A
- **Ramp** : Montée vers A
- **Apps** : Appartements
- **Underpass** : Passage sous Mid
- **Jungle** : Zone près de A
- **CT Spawn** : Spawn des CT

### 💬 Exemples de Communication :
- "Ennemi Connector !"
- "Ils rushent Apps !"
- "AWP Mid, smoke !"
- "Rotation B vers A !"

## 🛠️ Grenades Importantes

### 💣 Smokes Essentielles :
- **Mid** : Bloque la vue des CT
- **CT** : Bloque les rotations
- **Jungle** : Aide l'attaque A
- **Apps** : Aide l'attaque B

### ⚡ Flashbangs Utiles :
- **Ramp** : Aveugle les défenseurs A
- **Apps** : Aveugle les défenseurs B
- **Connector** : Aide les rotations

## 🏆 Objectif Final

Maîtriser Mirage te donne une **excellente base tactique** ! C'est la carte parfaite pour apprendre le jeu d'équipe.

**Prochaine étape** : Apprendre Inferno, une carte plus complexe !
`,
    tips: [
      'Apprends les smokes de base - elles sont essentielles sur Mirage',
      'Mid control est crucial - celui qui contrôle Mid contrôle la carte',
      'En Apps, regarde chaque angle - il y a beaucoup d\'endroits où se cacher',
      'Communique tes rotations - tes coéquipiers doivent savoir où tu vas',
      'Utilise les flashbangs - Mirage est parfaite pour les grenades'
    ],
    links: [
      { name: '🗺️ Mirage callouts interactive', url: 'https://www.simpleradar.com/mirage' },
      { name: '💣 Smokes Mirage tutorial', url: 'https://www.youtube.com/watch?v=mirage-smokes' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'maps-active-duty-inferno-basics': {
    title: 'Maps Active Duty : Inferno basics',
    level: 'Débutant',
    duration: '20 min',
    type: 'Maps',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Apprends Inferno, une carte complexe avec beaucoup d\'angles. Découvre les bases pour attaquer et défendre efficacement.',
    objectives: [
      'Comprendre la complexité d\'Inferno et ses nombreux angles',
      'Apprendre les routes principales (Apps, Arch, Alt Mid)',
      'Maîtriser les positions de base sur les sites A et B',
      'Comprendre l\'importance des grenades sur Inferno',
      'Savoir gérer les rotations sur cette carte fermée'
    ],
    content: `
# 🗺️ Inferno Basics - Les Bases

## 🎯 Pourquoi Inferno ?

Inferno est une carte **très complexe** avec beaucoup d'angles et de cachettes. Elle favorise légèrement les CT mais enseigne excellemment le jeu tactique !

## 🗺️ Plan d'Inferno

### 🎮 Zones Principales :
- **A Site** : Objectif A avec beaucoup d'angles
- **B Site** : Objectif B plus simple
- **Apartments** : Étages vers A
- **Mid** : Centre avec Alt Mid
- **Arch** : Passage vers A
- **Banana** : Passage vers B

### 🎯 Particularités :
- **Beaucoup d'angles** : Très technique
- **Avantage CT** : Plus facile à défendre
- **Grenades importantes** : Essentielles pour réussir

## 🎮 Côté Terrorist (Attaquants)

### 🎯 Stratégies Simples :
1. **Rush B Banana** : Tous vers B par Banana
2. **Apps Control** : Prendre les appartements vers A
3. **Arch Split** : Diviser l'attaque A
4. **Slow Round** : Prendre le temps, utiliser les grenades

### 🗺️ Routes d'Attaque :
- **Vers A** : T Spawn → Apps → Balcony → A Site
- **Vers A** : T Spawn → Mid → Arch → A Site
- **Vers B** : T Spawn → Banana → B Site
- **Alt Mid** : T Spawn → Alt Mid → support

## 🛡️ Côté Counter-Terrorist (Défenseurs)

### 🎯 Setup Standard :
- **3 joueurs A** : 1 Site + 1 Apps + 1 Arch
- **2 joueurs B** : 1 Site + 1 Banana
- **Rotations** : Difficiles, doivent être rapides

### 🎮 Avantages CT :
- **Beaucoup d'angles** : Facile de se cacher
- **Grenades efficaces** : Molotovs très utiles
- **Rotations** : Peuvent être rapides si bien jouées

## 🎯 Positions Détaillées

### 🏠 A Site (Très Complexe)
**Terrorists** :
- **Apps** : Appartements, route principale
- **Arch** : Passage alternatif
- **Balcony** : Depuis Apps vers Site
- **Conseils** : Utilise BEAUCOUP de grenades

**Counter-Terrorists** :
- **Site** : Beaucoup de positions (Truck, Default, etc.)
- **Apps** : Contrôle les appartements
- **Arch** : Surveille le passage
- **Conseils** : Communique constamment

### 🍌 B Site (Plus Simple)
**Terrorists** :
- **Banana** : Passage principal vers B
- **Mid** : Support depuis Alt Mid
- **Conseils** : Attention aux molotovs des CT

**Counter-Terrorists** :
- **Site B** : Défend le site
- **Banana** : Contrôle l'approche
- **Conseils** : Utilise les molotovs pour retarder

### 🎯 Mid (Alt Mid)
**Terrorists** :
- **Alt Mid** : Passage alternatif
- **Support** : Aide les attaques A et B
- **Conseils** : Difficile mais très utile

**Counter-Terrorists** :
- **Mid** : Surveille Alt Mid
- **Rotations** : Aide A et B
- **Conseils** : Position de support

## 🎮 Conseils pour Débutants

### ✅ Bonnes Pratiques :
- **Utilise BEAUCOUP de grenades** : Essentielles sur Inferno
- **Prends ton temps** : Ne rush pas sans réfléchir
- **Clear chaque angle** : Il y en a beaucoup
- **Communique** : Encore plus important que sur les autres cartes

### ❌ Erreurs Communes :
- Rusher sans grenades
- Ne pas clear les angles
- Mauvaise communication
- Ignorer Alt Mid

## 🎯 Stratégies Spécifiques

### 🍌 Rush B Banana (Facile)
**Plan** : Tous les 5 T vont vers B
**Execution** :
1. **Achetez** : Armor + armes + GRENADES
2. **Smoke Banana** : Bloque la vue CT
3. **Molotov** : Dégage les positions CT
4. **Rush** : Tous ensemble
5. **Plant** : Vite la bombe

### 🏠 Apps Control (Intermédiaire)
**Plan** : Prendre les appartements vers A
**Execution** :
1. **Setup** : 3-4 joueurs Apps
2. **Clear** : Chaque angle des appartements
3. **Smoke** : Balcony et Site
4. **Execute** : Attaque depuis Apps
5. **Support** : 1 joueur Arch

### 🎯 Arch Split (Avancé)
**Plan** : Diviser l'attaque A
**Execution** :
1. **Setup** : 2 Apps + 2 Arch + 1 support
2. **Timing** : Coordonner les deux attaques
3. **Grenades** : Beaucoup de smokes et flashs
4. **Execute** : Simultanément
5. **Trade** : Aide tes coéquipiers

## 🗺️ Callouts Importants

### 🎯 Noms des Positions :
- **A Site** : Le site A
- **B Site** : Le site B
- **Apps** : Appartements
- **Arch** : Passage vers A
- **Banana** : Passage vers B
- **Balcony** : Balcon des Apps
- **Alt Mid** : Mid alternatif
- **Truck** : Camion sur A
- **Default** : Position standard A

### 💬 Exemples de Communication :
- "Ennemi Apps étage 2 !"
- "Ils prennent Banana !"
- "AWP Arch, attention !"
- "Rotation Apps vers Arch !"

## 🛠️ Grenades Essentielles

### 💣 Smokes Cruciales :
- **Banana** : Bloque la vue vers B
- **Arch** : Aide l'attaque A
- **Balcony** : Protège la sortie Apps
- **CT** : Bloque les rotations

### 🔥 Molotovs Importantes :
- **Banana** : Dégage les positions CT
- **Apps** : Nettoie les angles
- **Site A** : Empêche les retakes
- **Site B** : Contrôle territorial

### ⚡ Flashbangs Utiles :
- **Apps** : Aveugle les défenseurs
- **Arch** : Aide l'attaque A
- **Banana** : Aveugle les CT

## 🏆 Objectif Final

Maîtriser Inferno te donne une **excellente compréhension tactique** ! C'est la carte parfaite pour apprendre l'usage avancé des grenades.

**Prochaine étape** : Apprendre l'utilisation des grenades de base !
`,
    tips: [
      'Inferno = grenades ! Achète toujours des grenades sur cette carte',
      'Prends ton temps - rusher sans préparation ne marche pas sur Inferno',
      'Apprends les smokes de base, surtout Banana et Arch',
      'Communique chaque ennemi vu - il y a trop d\'angles pour jouer seul',
      'En CT, utilise les molotovs pour retarder les attaques'
    ],
    links: [
      { name: '🗺️ Inferno callouts interactive', url: 'https://www.simpleradar.com/inferno' },
      { name: '🔥 Grenades Inferno tutorial', url: 'https://www.youtube.com/watch?v=inferno-grenades' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'utilisation-des-grenades-de-base': {
    title: 'Utilisation des grenades de base',
    level: 'Débutant',
    duration: '18 min',
    type: 'Utilities',
    image: 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à utiliser les grenades dans CS2. Découvre les HE grenades, flashbangs, smokes et molotovs avec des explications simples.',
    objectives: [
      'Comprendre les 4 types de grenades principales',
      'Apprendre à lancer correctement chaque grenade',
      'Savoir quand utiliser chaque type de grenade',
      'Maîtriser les techniques de base (popup, jumpthrow)',
      'Comprendre l\'importance des grenades dans la stratégie'
    ],
    content: `
# 💣 Utilisation des Grenades de Base

## 🎯 Pourquoi les Grenades ?

Les grenades sont **essentielles** dans CS2 ! Elles peuvent :
- Tuer des ennemis
- Aveugler les adversaires  
- Bloquer la vue
- Contrôler le territoire
- Créer des opportunités

## 🎮 Les 4 Types de Grenades

### 💥 HE Grenade (Explosive)
- **Prix** : 300$
- **Dégâts** : 57 maximum
- **Utilisation** : Blesser/tuer les ennemis
- **Touche** : 4 ou clic sur l'icône

### ⚡ Flashbang (Flash)
- **Prix** : 200$
- **Effet** : Aveugle les ennemis
- **Durée** : 1-7 secondes selon la distance
- **Utilisation** : Aveugler avant d'attaquer

### 💨 Smoke Grenade
- **Prix** : 300$
- **Effet** : Mur de fumée
- **Durée** : 18 secondes
- **Utilisation** : Bloquer la vue, avancer en sécurité

### 🔥 Molotov/Incendiary
- **Prix** : 400$
- **Effet** : Zone de feu
- **Durée** : 7 secondes
- **Utilisation** : Contrôler le territoire, empêcher le passage

## 🎯 HE Grenade (Explosive)

### 💥 Comment l'Utiliser :
1. **Équipe** la grenade (touche 4)
2. **Vise** où tu veux qu'elle explose
3. **Lance** (clic gauche)
4. **Attention** : Elle peut te blesser aussi !

### 🎮 Conseils d'Utilisation :
- **Timing** : Lance quand tu entends plusieurs ennemis
- **Cuisine** : Maintiens le clic pour réduire le délai
- **Combo** : Utilise après un flash ou smoke
- **Zones** : Parfait pour les passages étroits

### ✅ Bonnes Situations :
- Ennemis groupés dans un passage
- Retake de site (plusieurs ennemis)
- Finir un ennemi blessé derrière cover
- Eco rounds (pour économiser les balles)

## ⚡ Flashbang (Flash)

### 💡 Comment l'Utiliser :
1. **Équipe** la flashbang
2. **Vise** un mur ou le sol près des ennemis
3. **Lance** et **détourne-toi** immédiatement
4. **Attaque** pendant qu'ils sont aveuglés

### 🎯 Techniques de Lancer :
- **Popup Flash** : Lance vers le haut pour qu'elle explose en l'air
- **Bounce Flash** : Fait rebondir sur un mur
- **Clic droit** : Lancer court pour flash proche
- **Clic gauche** : Lancer long pour flash loin

### 🎮 Conseils Importants :
- **Ne regarde JAMAIS** ta propre flash
- **Tourne-toi** avant qu'elle explose
- **Time ton attaque** : Avance quand elle explose
- **Communique** : Préviens tes coéquipiers

## 💨 Smoke Grenade

### 🌪️ Comment l'Utiliser :
1. **Équipe** la smoke
2. **Vise** où tu veux le mur de fumée
3. **Lance** (clic gauche pour loin, clic droit pour proche)
4. **Attends** ~2 secondes avant qu'elle se déploie

### 🎯 Utilisations Tactiques :
- **Bloquer les snipers** : Smoke les angles longs
- **Avancer en sécurité** : Créer un mur protecteur
- **Diviser les ennemis** : Isoler une partie du site
- **Retakes** : Bloquer les angles défensifs

### 🎮 Conseils Stratégiques :
- **Placement** : Vise le sol où tu veux le centre
- **Timing** : Lance au bon moment (pas trop tôt)
- **Équipe** : Coordonne avec tes coéquipiers
- **Économie** : 300$ bien investis

## 🔥 Molotov/Incendiary

### 🔥 Comment l'Utiliser :
1. **Équipe** la molotov
2. **Vise** le sol où tu veux le feu
3. **Lance** (explose au contact)
4. **Attention** : Le feu peut t'atteindre aussi

### 🎯 Utilisations Tactiques :
- **Contrôler les angles** : Empêcher les ennemis de passer
- **Retarder les rushes** : Forcer les ennemis à attendre
- **Nettoyer les positions** : Déloger les ennemis
- **Post-plant** : Empêcher les retakes

### 🎮 Conseils d'Utilisation :
- **Angles étroits** : Très efficace dans les passages
- **Timing** : Lance au bon moment
- **Combine** : Utilise avec d'autres grenades
- **Attention** : Ne te brûle pas toi-même

## 🎯 Techniques de Lancer

### 🎮 Types de Lancer :
- **Clic gauche** : Lancer long et fort
- **Clic droit** : Lancer court et doux
- **Clic gauche + Clic droit** : Lancer moyen (maintenir les deux)

### 🎪 Jumpthrow (Saut-Lancer) :
1. **Prépare** ta grenade
2. **Cours** vers l'avant
3. **Saute** (Espace) et **lance** (Clic gauche) simultanément
4. **Résultat** : Lancer très long et précis

### 🎯 Popup Techniques :
- **Vise vers le haut** : Pour que la grenade explose en l'air
- **Bounce** : Utilise les murs pour des angles impossibles
- **Bank** : Fait rebondir sur plusieurs surfaces

## 🎮 Stratégies d'Équipe

### 🎯 Combos de Grenades :
1. **Smoke + Flash** : Avance en sécurité puis aveugle
2. **HE + Molotov** : Dégâts + contrôle territorial
3. **Flash + HE** : Aveugle puis explose
4. **Smoke + Molotov** : Bloque + contrôle

### 🎪 Économie des Grenades :
- **Full Buy** : 2-3 grenades par joueur
- **Eco Round** : 1 grenade maximum
- **Anti-Eco** : Grenades pour nettoyer
- **Retake** : Toujours des grenades

## 💡 Erreurs de Débutant

### ❌ Erreurs Communes :
- Se flasher soi-même
- Lancer les grenades trop tôt
- Gaspiller les grenades
- Ne pas communiquer l'utilisation

### ✅ Bonnes Habitudes :
- Toujours se détourner des flashs
- Coordonner avec l'équipe
- Économiser les grenades importantes
- Pratiquer les lancers sur des maps d'entraînement

## 🏆 Objectif Final

Maîtriser les grenades te donne un **avantage tactique énorme** ! Elles peuvent changer l'issue d'un round.

**Prochaine étape** : Apprendre le positionnement et les angles communs !
`,
    tips: [
      'Achète toujours au moins une grenade - elles sont essentielles',
      'Détourne-toi TOUJOURS de tes propres flashbangs',
      'Utilise les smokes pour bloquer les snipers - très efficace',
      'Entraîne-toi aux lancers sur des maps dédiées',
      'Communique quand tu utilises une grenade - préviens ton équipe'
    ],
    links: [
      { name: '💣 Maps d\'entraînement grenades', url: 'https://steamcommunity.com/workshop/browse/?appid=730&searchtext=grenades' },
      { name: '🎯 Jumpthrow bind tutorial', url: 'https://www.youtube.com/watch?v=jumpthrow-bind' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  }

,

  'positionnement-et-angles-communs': {
    title: 'Positionnement et angles communs',
    level: 'Débutant',
    duration: '17 min',
    type: 'Positioning',
    image: 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw1fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à te positionner correctement dans CS2. Découvre les angles importants et comment les utiliser à ton avantage.',
    objectives: [
      'Comprendre l\'importance du positionnement',
      'Apprendre à utiliser les angles (wide peek, tight peek)',
      'Connaître les positions communes sur les cartes',
      'Savoir quand changer de position après un kill',
      'Maîtriser les bases du cover et des abris'
    ],
    content: `
# 🎯 Positionnement et Angles Communs

## 🎮 Pourquoi le Positionnement ?

Le **positionnement** est crucial dans CS2. Une bonne position peut :
- Te donner l'avantage sur l'ennemi
- Te protéger des tirs
- Te permettre de fuir si nécessaire
- Surprendre tes adversaires

## 🎯 Les Angles de Base

### 👁️ Wide Peek (Angle Large)
- **Technique** : Sors loin de l'angle
- **Avantage** : Tu vois l'ennemi en premier
- **Inconvénient** : Tu es exposé plus longtemps
- **Quand utiliser** : Quand tu es sûr qu'il y a un ennemi

### 🎪 Tight Peek (Angle Serré)
- **Technique** : Sors près de l'angle
- **Avantage** : Tu peux te cacher rapidement
- **Inconvénient** : L'ennemi peut te voir en premier
- **Quand utiliser** : Quand tu n'es pas sûr

### 🎯 Shoulder Peek (Montrer l'Épaule)
- **Technique** : Montre juste ton épaule
- **But** : Faire tirer l'ennemi pour connaître sa position
- **Avantage** : Tu récupères l'info sans risquer ta vie
- **Timing** : Très rapide

## 🏠 Utiliser les Abris (Cover)

### 🎮 Types d'Abris :
- **Murs** : Protection complète
- **Caisses** : Protection partielle
- **Angles** : Protection temporaire
- **Dénivelés** : Protection contre certains angles

### 🎯 Règles du Cover :
1. **Toujours près d'un abri** : Pour pouvoir te cacher
2. **Plusieurs sorties** : Ne te fais pas piéger
3. **Angles multiples** : Évite les positions exposées
4. **Distance** : Reste à bonne distance des angles

## 🎯 Positions Communes

### 🎮 Positions Défensives (CT) :
- **Anchor** : Défend un site seul
- **Rotate** : Bouge selon les besoins
- **Support** : Aide les autres joueurs
- **Lurk** : Position isolée pour l'information

### 🎯 Positions Offensives (T) :
- **Entry** : Premier à entrer sur un site
- **Support** : Aide l'entry fragger
- **Lurk** : Isolé pour surprendre
- **IGL** : Dirige l'équipe depuis l'arrière

## 🎮 Changement de Position

### 🎯 Quand Changer de Position :
- **Après un kill** : L'ennemi connaît ta position
- **Si tu es repéré** : Ils savent où tu es
- **Bruit suspect** : Ils arrivent vers toi
- **Ordre de l'équipe** : Rotation demandée

### 🎪 Comment Changer de Position :
1. **Discrètement** : Marche avec Shift
2. **Rapidement** : Si tu es découvert
3. **Communique** : Dis où tu vas
4. **Couvre** : Aide tes coéquipiers

## 🗺️ Positionnement par Carte

### 🏜️ Dust2 :
- **Long A** : Derrière les caisses, dans le coin
- **Short A** : Sur la plateforme, derrière les caisses
- **Mid** : Derrière les caisses, sur Xbox
- **Site B** : Dans les coins, derrière les caisses

### 🎯 Mirage :
- **A Site** : Derrière les caisses, dans les coins
- **B Site** : Angles multiples, utilise les murs
- **Mid** : Positions élevées, derrière cover
- **Connector** : Angles serrés, protection

### 🏠 Inferno :
- **A Site** : Beaucoup d'angles, utilise tous les covers
- **B Site** : Positions diverses, change souvent
- **Mid** : Positions de support, mobility

## 🎮 Erreurs de Positionnement

### ❌ Erreurs Communes :
- **Rester au même endroit** : Prévisible
- **Pas d'abri** : Facile à tuer
- **Mauvais angles** : Désavantagé
- **Pas de sortie** : Piégé

### ✅ Bonnes Pratiques :
- **Change régulièrement** : Reste imprévisible
- **Toujours près d'un abri** : Sécurité
- **Plusieurs sorties** : Flexibilité
- **Communique** : Informe l'équipe

## 🎯 Techniques Avancées

### 🎮 Off-Angles :
- **Définition** : Positions non-standard
- **Avantage** : Surprise l'ennemi
- **Inconvénient** : Difficile à tenir
- **Utilisation** : Occasionnelle

### 🎪 Baiting :
- **Technique** : Attirer l'ennemi
- **But** : Lui faire prendre un mauvais angle
- **Risque** : Tu peux mourir
- **Récompense** : Ton équipe a l'avantage

### 🎯 Trading :
- **Principe** : Venger un coéquipier mort
- **Position** : Près de ton coéquipier
- **Timing** : Immédiat après sa mort
- **Résultat** : Échange 1 contre 1

## 💡 Conseils Pratiques

### 🎮 Pour Débutants :
- **Commence simple** : Positions standard
- **Observe** : Regarde où les pros se placent
- **Pratique** : Essaie différentes positions
- **Patience** : Le bon positionnement prend du temps

### 🎯 Développement :
1. **Semaine 1** : Positions de base
2. **Semaine 2** : Changements de position
3. **Semaine 3** : Angles avancés
4. **Semaine 4** : Positions créatives

## 🏆 Objectif Final

Le **bon positionnement** peut te faire gagner des duels même si tu vises moins bien ! C'est un avantage stratégique énorme.

**Prochaine étape** : Apprendre la communication efficace avec l'équipe !
`,
    tips: [
      'Change toujours de position après un kill - ils savent où tu es',
      'Garde toujours un abri proche pour pouvoir te cacher',
      'Utilise les off-angles occasionnellement pour surprendre',
      'Observe les positions des joueurs pro sur les streams',
      'Pratique différentes positions sur chaque carte'
    ],
    links: [
      { name: '🎯 Positions populaires par carte', url: 'https://www.hltv.org/stats' },
      { name: '📹 Positionnement pro analysis', url: 'https://www.youtube.com/watch?v=positioning-cs2' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'communication-team-efficace': {
    title: 'Communication team efficace',
    level: 'Débutant',
    duration: '15 min',
    type: 'Communication',
    image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à communiquer efficacement avec ton équipe. Découvre les callouts importantes et comment donner les bonnes informations.',
    objectives: [
      'Comprendre l\'importance de la communication',
      'Apprendre les callouts de base des cartes populaires',
      'Savoir donner des informations utiles et précises',
      'Maîtriser les commandes de communication (voice, chat)',
      'Développer un bon esprit d\'équipe'
    ],
    content: `
# 💬 Communication Team Efficace

## 🎯 Pourquoi Communiquer ?

La **communication** est essentielle dans CS2 ! Elle permet de :
- Partager des informations sur les ennemis
- Coordonner les stratégies
- Aider les coéquipiers
- Gagner plus de rounds

## 🎮 Les Bases de la Communication

### 🎤 Voice Chat (Voix)
- **Touche** : Par défaut "K" (maintenir)
- **Utilisation** : Informations importantes
- **Timing** : Rapide et précis
- **Qualité** : Micro clair

### 💬 Text Chat (Texte)
- **Touche** : "Y" (équipe) ou "U" (tous)
- **Utilisation** : Infos moins urgentes
- **Avantage** : Reste visible
- **Inconvénient** : Plus lent

### 🎯 Commandes Utiles :
- **"Y"** : Chat équipe
- **"U"** : Chat tous
- **"K"** : Voice chat (maintenir)
- **TAB** : Mute/unmute joueurs

**Note AZERTY** : Sur clavier français, la touche "Y" est à la place du "Z" sur QWERTY.

## 🗺️ Callouts Essentiels

### 🏜️ Dust2 :
- **"Long A"** : Le long couloir
- **"Short A"** / **"Cat"** : Les escaliers
- **"Mid"** : Le centre
- **"Tunnels"** : Passage vers B
- **"Site A"** / **"Site B"** : Les objectifs
- **"CT Spawn"** : Spawn des CT

### 🎯 Mirage :
- **"A Site"** : Objectif A
- **"B Site"** : Objectif B
- **"Mid"** : Centre
- **"Connector"** : Lien Mid-A
- **"Ramp"** : Montée vers A
- **"Apps"** : Appartements

### 🏠 Inferno :
- **"A Site"** : Objectif A
- **"B Site"** : Objectif B
- **"Apps"** : Appartements
- **"Arch"** : Passage vers A
- **"Banana"** : Passage vers B
- **"Mid"** : Centre

## 🎯 Informations Importantes

### 📍 Position des Ennemis :
- **"Ennemi Long A"** : Précis et utile
- **"Il y a quelqu'un"** : Trop vague
- **"AWP Mid"** : Spécifique et important
- **"Ils rushent B"** : Urgent et clair

### 🎮 Nombre d'Ennemis :
- **"Un ennemi Long A"** : Précis
- **"Deux Mid"** : Très utile
- **"Ils sont tous B"** : Information cruciale
- **"Quelques-uns"** : Pas assez précis

### 🎯 Armes Importantes :
- **"AWP Long A"** : Attention sniper
- **"AK Mid"** : Arme puissante
- **"Pistolets seulement"** : Ils sont en eco
- **"Full buy"** : Ils ont de l'argent

## 🎮 Quand Communiquer

### ✅ Toujours Communiquer :
- **Ennemi repéré** : Position exacte
- **Mort** : Où tu es mort et combien
- **Informations** : Nombre d'ennemis
- **Stratégie** : Plans d'équipe

### ❌ Ne Pas Communiquer :
- **Pendant les clutchs** : Laisse le joueur se concentrer
- **Informations anciennes** : Pas utiles
- **Critiques** : Reste positif
- **Spam** : Trop d'informations

## 🎯 Communication Efficace

### 🎮 Structure d'une Bonne Communication :
1. **Où** : Position précise
2. **Combien** : Nombre d'ennemis
3. **Quoi** : Armes/équipement
4. **Quand** : Timing (si important)

### 📢 Exemples :
- **"Deux ennemis Long A, AK et AWP"**
- **"Un Mid, il rotate vers B"**
- **"Ils plantent A, dépêchez-vous"**
- **"AWP Mid, smoke demandée"**

## 💬 Ton et Attitude

### ✅ Bon Esprit :
- **Positif** : Encourage l'équipe
- **Calme** : Même en situation tendue
- **Constructif** : Aide à améliorer
- **Respectueux** : Reste poli

### ❌ Mauvais Esprit :
- **Toxique** : Critique méchamment
- **Panique** : Stress l'équipe
- **Spam** : Parle trop
- **Blame** : Accuse les autres

## 🎮 Communication Stratégique

### 🎯 Coordination d'Équipe :
- **"On va B tous ensemble"**
- **"Split A : 3 Ramp, 2 Connector"**
- **"Eco round, gardez votre argent"**
- **"Full buy, on prend A"**

### 🎪 Appels Tactiques :
- **"Smoke Mid s'il vous plaît"**
- **"Flash pour moi"**
- **"Trade-moi si je meurs"**
- **"Rotate B, ils sont tous A"**

## 🎯 Après la Mort

### 🎮 Informations Utiles :
- **Où tu es mort** : Position exacte
- **Combien d'ennemis** : Nombre vu
- **Leurs HP** : Si tu as blessé
- **Leurs positions** : Dernières vues

### 🎪 Exemple :
**"Mort Long A, un ennemi derrière les caisses, il lui reste 30 HP"**

## 💡 Conseils Pratiques

### 🎮 Pour Débutants :
- **Commence simple** : Positions de base
- **Écoute** : Apprends des autres
- **Pratique** : Utilise les callouts
- **Patience** : Améliore-toi progressivement

### 🎯 Développement :
1. **Apprends les callouts** : Une carte à la fois
2. **Pratique la voix** : Sois clair et rapide
3. **Développe l'esprit** : Reste positif
4. **Écoute les pros** : Regarde les streams

## 🏆 Objectif Final

Une **bonne communication** peut faire la différence entre une équipe moyenne et une équipe gagnante !

**Prochaine étape** : Apprendre les routines d'échauffement !
`,
    tips: [
      'Apprends les callouts de base - c\'est essentiel pour communiquer',
      'Sois précis et rapide - "Un ennemi Long A" est mieux que "Il y a quelqu\'un"',
      'Reste positif même quand ça va mal - l\'équipe a besoin de moral',
      'Ne parle pas pendant les clutchs - laisse le joueur se concentrer',
      'Communique même après ta mort - tes infos peuvent sauver le round'
    ],
    links: [
      { name: '🗺️ Callouts interactifs toutes cartes', url: 'https://www.simpleradar.com' },
      { name: '🎤 Configuration micro CS2', url: 'https://www.youtube.com/watch?v=mic-setup-cs2' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'rounds-d-echauffement-et-warm-up': {
    title: 'Rounds d\'échauffement et warm-up',
    level: 'Débutant',
    duration: '12 min',
    type: 'Training',
    image: 'https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à t\'échauffer efficacement avant de jouer. Découvre les routines d\'entraînement pour améliorer ta précision.',
    objectives: [
      'Comprendre l\'importance de l\'échauffement',
      'Apprendre une routine d\'échauffement efficace',
      'Découvrir les maps d\'entraînement essentielles',
      'Maîtriser les exercices de visée de base',
      'Développer une routine quotidienne'
    ],
    content: `
# 🎯 Rounds d'Échauffement et Warm-up

## 🎮 Pourquoi s'Échauffer ?

L'**échauffement** est crucial avant de jouer ! Il permet de :
- Améliorer ta précision
- Préparer tes réflexes
- Tester tes paramètres
- Prendre confiance

## 🎯 Routine d'Échauffement (15 minutes)

### 🎮 Phase 1 : Échauffement Basique (5 min)
1. **aim_botz** : Tir sur bots immobiles
   - **Objectif** : Précision pure
   - **Durée** : 2 minutes
   - **Focus** : Headshots uniquement

2. **Spray Control** : Contrôle du recul
   - **Mur** : Tire sur un mur
   - **Durée** : 1 minute AK + 1 minute M4
   - **Focus** : Pattern de recul

3. **Tracking** : Suivre les cibles
   - **aim_botz** : Bots qui bougent
   - **Durée** : 1 minute
   - **Focus** : Suivre le mouvement

### 🎪 Phase 2 : Exercices Avancés (7 min)
1. **Flicking** : Mouvements rapides
   - **aim_redline** : Cibles qui apparaissent
   - **Durée** : 3 minutes
   - **Focus** : Réaction rapide

2. **Movement + Aim** : Bouger et viser
   - **aim_botz** : Strafing + tir
   - **Durée** : 2 minutes
   - **Focus** : Tir en mouvement

3. **Prefire** : Pré-visée
   - **yprac_maps** : Angles communs
   - **Durée** : 2 minutes
   - **Focus** : Angles de la carte du jour

### 🎯 Phase 3 : Preparation Match (3 min)
1. **Deathmatch** : Combat réel
   - **Durée** : 3 minutes
   - **Focus** : Conditions réelles
   - **Objectif** : Confiance

## 🗺️ Maps d'Entraînement Essentielles

### 🎯 aim_botz :
- **Type** : Précision pure
- **Usage** : Échauffement quotidien
- **Exercices** : Headshots, flicking, tracking
- **Avantage** : Simple et efficace

### 🎪 aim_redline :
- **Type** : Réaction rapide
- **Usage** : Améliorer les réflexes
- **Exercices** : Flicking, timing
- **Avantage** : Cibles mobiles

### 🎮 training_aim_csgo2 :
- **Type** : Exercices variés
- **Usage** : Entraînement complet
- **Exercices** : Multiples scenarios
- **Avantage** : Très complet

### 🗺️ yprac_maps :
- **Type** : Entraînement carte spécifique
- **Usage** : Prefire, angles
- **Exercices** : Angles réels
- **Avantage** : Pratique réelle

## 🎯 Exercices Spécifiques

### 🎮 Headshot Only :
- **Objectif** : Améliorer la précision
- **Méthode** : Vise uniquement la tête
- **Durée** : 2-3 minutes
- **Bénéfice** : Meilleure précision

### 🎪 Spray Control :
- **Objectif** : Maîtriser le recul
- **Méthode** : Tire sur un mur, corrige le recul
- **Durée** : 1 minute par arme
- **Bénéfice** : Meilleur contrôle

### 🎯 Flicking :
- **Objectif** : Réaction rapide
- **Méthode** : Vise rapidement différentes cibles
- **Durée** : 3-5 minutes
- **Bénéfice** : Meilleurs réflexes

### 🎮 Movement + Aim :
- **Objectif** : Tir en mouvement
- **Méthode** : Bouge et tire simultanément
- **Durée** : 2 minutes
- **Bénéfice** : Meilleur dans les combats

## 🎯 Routine Quotidienne

### 🌅 Routine Courte (10 min) :
1. **aim_botz** : 3 minutes headshots
2. **Spray control** : 2 minutes
3. **Flicking** : 3 minutes
4. **Deathmatch** : 2 minutes

### 🎮 Routine Normale (15 min) :
1. **aim_botz** : 5 minutes variés
2. **aim_redline** : 3 minutes
3. **Spray control** : 2 minutes
4. **Prefire** : 2 minutes
5. **Deathmatch** : 3 minutes

### 🎯 Routine Longue (25 min) :
1. **aim_botz** : 7 minutes
2. **aim_redline** : 5 minutes
3. **Spray control** : 3 minutes
4. **Movement + aim** : 3 minutes
5. **Prefire** : 2 minutes
6. **Deathmatch** : 5 minutes

## 🎮 Conseils d'Entraînement

### ✅ Bonnes Pratiques :
- **Régularité** : Tous les jours
- **Progression** : Augmente la difficulté
- **Patience** : Les résultats prennent du temps
- **Variété** : Change les exercices

### ❌ Erreurs Communes :
- **Trop long** : Fatigue inutile
- **Pas assez** : Pas d'amélioration
- **Monotone** : Toujours les mêmes exercices
- **Impatience** : Vouloir des résultats immédiats

## 🎯 Paramètres d'Entraînement

### 🎮 Sensitivity :
- **Garde la même** : Consistance importante
- **Teste avant** : Vérifie que c'est bon
- **Ajuste si besoin** : Mais évite les changements fréquents

### 🎪 Crosshair :
- **Utilise le tien** : Pas celui de la map
- **Teste la visibilité** : Assure-toi qu'il soit visible
- **Reste cohérent** : Même crosshair partout

## 💡 Conseils Pratiques

### 🎮 Pour Débutants :
- **Commence simple** : aim_botz seulement
- **Sois patient** : Les résultats viennent
- **Écoute ton corps** : Arrête si tu fatigues
- **Varie les exercices** : Évite la monotonie

### 🎯 Progression :
1. **Semaine 1** : aim_botz uniquement
2. **Semaine 2** : Ajoute spray control
3. **Semaine 3** : Ajoute flicking
4. **Semaine 4** : Routine complète

## 🏆 Objectif Final

Un **bon échauffement** peut améliorer tes performances de 20-30% ! C'est un investissement qui vaut la peine.

**Prochaine étape** : Apprendre les paramètres audio !
`,
    tips: [
      'Échauffe-toi TOUJOURS avant de jouer - même 5 minutes font la différence',
      'Garde une routine consistante - ton cerveau s\'habitue aux exercices',
      'Ne t\'échauffe pas trop longtemps - 15 minutes suffisent',
      'Varie les exercices pour éviter la monotonie',
      'Écoute ton corps - arrête si tu fatigues'
    ],
    links: [
      { name: '🎯 aim_botz map download', url: 'https://steamcommunity.com/sharedfiles/filedetails/?id=243702660' },
      { name: '🎪 Routines d\'échauffement pros', url: 'https://www.youtube.com/watch?v=warmup-cs2' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'parametres-audio-et-son-directionnel': {
    title: 'Paramètres audio et son directionnel',
    level: 'Débutant',
    duration: '14 min',
    type: 'Settings',
    image: 'https://images.unsplash.com/photo-1545558014-8692077e9b5c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxhdWRpb3xlbnwwfHx8fDE3NTMzMTQ5NDh8MA&ixlib=rb-4.1.0&q=85',
    description: 'Configure ton audio pour avoir un avantage dans CS2. Apprends à entendre et localiser les ennemis grâce au son.',
    objectives: [
      'Comprendre l\'importance du son dans CS2',
      'Configurer les paramètres audio optimaux',
      'Apprendre à localiser les ennemis par le son',
      'Maîtriser les différents bruits du jeu',
      'Choisir le bon équipement audio'
    ],
    content: `
# 🎧 Paramètres Audio et Son Directionnel

## 🎯 Pourquoi l'Audio est Crucial ?

Le **son** dans CS2 est **aussi important que la vue** ! Il te permet de :
- Localiser les ennemis
- Comprendre leurs mouvements
- Anticiper leurs actions
- Avoir un avantage tactique

## 🎮 Paramètres Audio Recommandés

### 🎧 Paramètres In-Game :
\`\`\`
Master Volume: 0.5-0.8
Music Volume: 0 (désactivé)
Voice Volume: 0.3-0.5
Sound Effects: 1.0 (maximum)
\`\`\`

### 🎯 Paramètres Audio Avancés :
\`\`\`
Audio Device: Speakers/Headphones
Advanced 3D Audio Processing: Enabled
\`\`\`

### 🎪 Commandes Console :
\`\`\`
snd_mixahead "0.025"
snd_headphone_pan_exponent "1.2"
snd_front_headphone_position "45"
snd_rear_headphone_position "90"
\`\`\`

## 🎧 Équipement Audio

### 🎮 Casques Recommandés :
- **Casque fermé** : Meilleure isolation
- **Bonne qualité** : Pas forcément gaming
- **Confortable** : Pour les longues sessions
- **Micro intégré** : Pour la communication

### 🎯 Types d'Écouteurs :
- **Over-ear** : Meilleure qualité sonore
- **On-ear** : Plus légers
- **In-ear** : Portables mais moins précis
- **Gaming headset** : Optimisés pour les jeux

### 🎪 Conseils d'Achat :
- **Budget** : 50-150€ suffisent
- **Marques** : Audio-Technica, Sennheiser, HyperX
- **Évite** : Casques "gaming" trop chers
- **Teste** : Si possible avant d'acheter

## 🎯 Sons Importants à Reconnaître

### 🚶 Bruits de Pas :
- **Course** : Très audible, rythme rapide
- **Marche** : Moins audible, rythme lent
- **Saut** : Bruit d'atterrissage distinct
- **Échelles** : Son métallique particulier

### 🔫 Bruits d'Armes :
- **Rechargement** : Chaque arme a son son
- **Dégainer** : Changement d'arme
- **Sécurité** : Retirer le silencieux
- **Munitions** : Ramasser des munitions

### 🎮 Bruits d'Environnement :
- **Grenades** : Goupille, explosion
- **Planting** : Bruit de la bombe
- **Defusing** : Désamorçage
- **Portes** : Ouverture/fermeture

## 🎯 Localisation Sonore

### 🎧 Principe de Base :
- **Oreille gauche** : Ennemi à gauche
- **Oreille droite** : Ennemi à droite
- **Les deux** : Ennemi devant/derrière
- **Volume** : Distance approximative

### 🎮 Techniques d'Écoute :
1. **Arrête-toi** : Pour mieux entendre
2. **Tourne la tête** : Change l'angle d'écoute
3. **Analyse** : Type de bruit + direction
4. **Communique** : Partage l'info

### 🎯 Difficultés Communes :
- **Devant/Derrière** : Difficile à distinguer
- **Haut/Bas** : Selon les cartes
- **Distance** : Prend de l'expérience
- **Bruits multiples** : Confusion possible

## 🗺️ Son par Carte

### 🏜️ Dust2 :
- **Long A** : Écho caractéristique
- **Tunnels** : Son fermé et réverbérant
- **Mid** : Sons ouverts
- **Sites** : Échos différents

### 🎯 Mirage :
- **Apps** : Échos d'appartement
- **Mid** : Son ouvert
- **Sites** : Réverbération
- **Connector** : Passage étroit

### 🏠 Inferno :
- **Beaucoup d'échos** : Environnement complexe
- **Apps** : Sons d'étages
- **Banana** : Couloir fermé
- **Sites** : Échos variés

## 🎮 Stratégies Audio

### 🎯 Écoute Active :
- **Pause régulière** : Arrête-toi pour écouter
- **Silence radio** : Demande le silence
- **Concentration** : Focus sur l'audio
- **Interprétation** : Comprends ce que tu entends

### 🎪 Information Gathering :
- **Nombre d'ennemis** : Compte les pas
- **Direction** : Où ils vont
- **Timing** : Quand ils arrivent
- **Armes** : Quel équipement ils ont

## 🎯 Erreurs Audio Communes

### ❌ Erreurs de Débutants :
- **Musique trop forte** : Masque les bruits importants
- **Pas d'écoute** : Cours tout le temps
- **Mauvais équipement** : Écouteurs de mauvaise qualité
- **Confusion** : Confond ses bruits avec ceux des ennemis

### ✅ Bonnes Pratiques :
- **Musique à 0** : Désactive complètement
- **Écoute régulière** : Arrête-toi souvent
- **Bon équipement** : Investis dans un casque décent
- **Pratique** : Développe ton oreille

## 💡 Conseils Pratiques

### 🎮 Pour Développer son Oreille :
1. **Joue sans son** : Puis avec, pour comparer
2. **Écoute des démos** : Analyse les sons
3. **Pratique** : Régulièrement
4. **Patience** : Ça prend du temps

### 🎯 Environnement :
- **Pièce calme** : Moins de distractions
- **Ferme les fenêtres** : Évite les bruits extérieurs
- **Informe** : Préviens ta famille/colocataires
- **Concentration** : Éteins les autres sons

## 🏆 Objectif Final

Un **bon audio** peut te donner un avantage de 30-40% ! C'est souvent ce qui fait la différence entre les bons joueurs.

**Prochaine étape** : Apprendre la gestion du stress !
`,
    tips: [
      'Désactive la musique complètement - elle masque les bruits importants',
      'Investis dans un bon casque - c\'est aussi important que la souris',
      'Arrête-toi régulièrement pour écouter - l\'info audio est cruciale',
      'Apprends à reconnaître les différents bruits de pas',
      'Pratique l\'écoute directionnelle - ça prend du temps mais c\'est essentiel'
    ],
    links: [
      { name: '🎧 Guide casques CS2', url: 'https://www.youtube.com/watch?v=headphones-cs2' },
      { name: '🎯 Paramètres audio pros', url: 'https://prosettings.net/cs2/audio/' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'gestion-du-stress-et-mental-game': {
    title: 'Gestion du stress et mental game',
    level: 'Débutant',
    duration: '16 min',
    type: 'Mental',
    image: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxtZW50YWwlMjBoZWFsdGh8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Apprends à gérer ton stress et améliorer ton mental dans CS2. Découvre comment rester calme et performant sous pression.',
    objectives: [
      'Comprendre l\'impact du mental sur les performances',
      'Apprendre à gérer le stress pendant les matchs',
      'Développer une mentalité positive',
      'Maîtriser les techniques de relaxation',
      'Améliorer sa concentration et focus'
    ],
    content: `
# 🧠 Gestion du Stress et Mental Game

## 🎯 Pourquoi le Mental est Important ?

Le **mental** représente **50% de tes performances** dans CS2 ! Il influence :
- Ta précision sous pression
- Tes prises de décision
- Ta communication
- Ton plaisir de jeu

## 🎮 Types de Stress en CS2

### 😰 Stress de Performance :
- **Clutch situations** : 1v3, 1v4, 1v5
- **Rounds importants** : 15-15, match point
- **Pressure** : Équipe qui compte sur toi
- **Ranking** : Peur de perdre son rang

### 🎯 Stress Social :
- **Toxicité** : Équipe qui blame
- **Jugement** : Peur du ridicule
- **Communication** : Micro anxiety
- **Nouveaux joueurs** : Peur de mal faire

### 🎪 Stress Technique :
- **Aim off** : Précision qui baisse
- **Mauvaises décisions** : Erreurs répétées
- **Tilt** : Frustration qui s'accumule
- **Losing streak** : Série de défaites

## 🎯 Techniques de Relaxation

### 🧘 Respiration :
1. **Inspire** : 4 secondes par le nez
2. **Retiens** : 4 secondes
3. **Expire** : 6 secondes par la bouche
4. **Répète** : 3-5 fois

### 🎮 Relaxation Musculaire :
- **Contracte** : Tous tes muscles 5 secondes
- **Relâche** : Sensation de détente
- **Répète** : 2-3 fois
- **Focus** : Sur la relaxation

### 🎯 Visualisation :
- **Imagine** : Toi en train de réussir
- **Détails** : Précision, kills, victoire
- **Répète** : Régulièrement
- **Confiance** : Crois en tes capacités

## 🎮 Mental Pendant le Match

### 🎯 Avant le Match :
- **Échauffement** : Prépare ton corps
- **Mindset** : Pense positif
- **Objectifs** : Fixe-toi des buts réalistes
- **Relaxation** : Évacue le stress

### 🎪 Pendant le Match :
- **Focus** : Concentre-toi sur le présent
- **Positif** : Encourage ton équipe
- **Analyse** : Apprends de tes erreurs
- **Patience** : Reste calme

### 🎮 Après le Match :
- **Analyse** : Qu'est-ce qui a marché/pas marché
- **Positif** : Trouve les points positifs
- **Amélioration** : Que peux-tu améliorer
- **Repos** : Prends une pause si nécessaire

## 🎯 Gérer les Situations Stressantes

### 🎪 Clutch Situations :
1. **Respire** : Ralentis ton rythme cardiaque
2. **Évalue** : Analyse la situation
3. **Plan** : Décide d'une stratégie
4. **Execute** : Reste calme et précis

### 🎮 Rounds Importants :
- **Routine** : Fais comme d'habitude
- **Confiance** : Tu peux y arriver
- **Équipe** : Communique normalement
- **Pression** : Transforme-la en motivation

### 🎯 Mauvaises Passes :
- **Pause** : Prends une petite pause
- **Analyse** : Qu'est-ce qui ne va pas
- **Ajuste** : Change quelque chose
- **Persévère** : Ça va s'améliorer

## 🧠 Développer une Mentalité Positive

### ✅ Pensées Positives :
- **"Je peux y arriver"** : Confiance en soi
- **"C'est un défi"** : Motivation
- **"Je m'améliore"** : Growth mindset
- **"Mon équipe compte sur moi"** : Responsabilité

### ❌ Pensées Négatives :
- **"Je suis nul"** : Destructeur
- **"C'est impossible"** : Démotivant
- **"J'ai de la malchance"** : Victim mindset
- **"Mes coéquipiers sont nuls"** : Toxique

### 🎮 Transformation :
- **Identifie** : Tes pensées négatives
- **Remplace** : Par des pensées positives
- **Répète** : Jusqu'à ce que ça devienne naturel
- **Crois** : En tes capacités

## 🎯 Gestion de la Toxicité

### 🎮 Si tu es Toxique :
1. **Reconnais** : Que tu as un problème
2. **Respire** : Avant de parler
3. **Pense** : Est-ce que ça va aider ?
4. **Communique** : Constructivement

### 🎪 Si les Autres sont Toxiques :
- **Mute** : N'hésite pas à couper le son
- **Ignore** : Ne réponds pas aux provocations
- **Focus** : Sur ton jeu
- **Report** : Les comportements inacceptables

## 💡 Conseils Pratiques

### 🎮 Routine Anti-Stress :
1. **Avant de jouer** : 5 minutes de relaxation
2. **Pendant** : Respiration entre les rounds
3. **Après** : Analyse positive
4. **Régulièrement** : Pauses si nécessaire

### 🎯 Amélioration Continue :
- **Journal** : Note tes progrès
- **Objectifs** : Fixe-toi des buts
- **Patience** : Les résultats prennent du temps
- **Persévérance** : Continue même si c'est difficile

### 🎪 Environnement :
- **Confortable** : Chaise, température
- **Hydratation** : Bois régulièrement
- **Pauses** : Toutes les heures
- **Sommeil** : Repos suffisant

## 🏆 Objectif Final

Un **bon mental** peut transformer tes performances ! C'est souvent ce qui sépare les joueurs moyens des bons joueurs.

**Prochaine étape** : Apprendre la routine pré-match !
`,
    tips: [
      'Respire profondément entre les rounds - ça aide à rester calme',
      'Transforme le stress en excitation - c\'est la même énergie',
      'Mute les joueurs toxiques sans hésiter - protège ton mental',
      'Fixe-toi des objectifs réalistes - ne vise pas trop haut',
      'Prends des pauses régulières - le mental se fatigue aussi'
    ],
    links: [
      { name: '🧠 Mental coaching esports', url: 'https://www.youtube.com/watch?v=mental-esports' },
      { name: '🎯 Techniques de relaxation', url: 'https://www.headspace.com/meditation/gaming' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  },

  'routine-pre-match-et-preparation': {
    title: 'Routine pré-match et préparation',
    level: 'Débutant',
    duration: '13 min',
    type: 'Preparation',
    image: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw2fHxtZW50YWwlMjBoZWFsdGh8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    description: 'Développe une routine pré-match efficace. Apprends à te préparer mentalement et techniquement avant chaque partie.',
    objectives: [
      'Créer une routine pré-match personnalisée',
      'Préparer son équipement et ses paramètres',
      'Se préparer mentalement pour la compétition',
      'Vérifier ses réglages et sa configuration',
      'Développer des habitudes gagnantes'
    ],
    content: `
# 🎯 Routine Pré-Match et Préparation

## 🎮 Pourquoi une Routine Pré-Match ?

Une **routine pré-match** te permet de :
- Être consistent dans tes performances
- Réduire le stress et l'anxiété
- Vérifier que tout fonctionne
- Te mettre dans le bon état d'esprit

## 🎯 Routine Pré-Match Complète (30 min)

### 🖥️ Phase 1 : Préparation Technique (10 min)

#### ⚙️ Vérification Matériel :
- **Souris** : Nettoie-la, vérifie les piles
- **Clavier** : Fonctionne correctement
- **Casque** : Audio et micro OK
- **Écran** : Luminosité et netteté

#### 🎮 Paramètres CS2 :
- **Sensibilité** : Vérifie qu'elle n'a pas changé
- **Crosshair** : Ton crosshair habituel
- **Binds** : Toutes les touches fonctionnent
- **Audio** : Volume et paramètres

#### 💻 Système :
- **FPS** : Vérifie que tu as de bons FPS
- **Ping** : Teste ta connexion
- **Drivers** : Tout est à jour
- **Programmes** : Ferme les apps inutiles

### 🎯 Phase 2 : Échauffement (15 min)

#### 🎮 Échauffement Aim (10 min) :
1. **aim_botz** : 3 min headshots
2. **Spray control** : 2 min
3. **Flicking** : 3 min
4. **Tracking** : 2 min

#### 🎪 Échauffement Mental (5 min) :
- **Deathmatch** : Combat réel
- **Confiance** : Prends confiance
- **Timing** : Habitue-toi au rythme
- **Feeling** : Trouve ton feeling

### 🧠 Phase 3 : Préparation Mentale (5 min)

#### 🎯 Relaxation :
- **Respiration** : 3 minutes de respiration profonde
- **Visualisation** : Imagine-toi réussir
- **Objectifs** : Fixe-toi des buts pour le match
- **Confiance** : Rappelle-toi tes succès

## 🎮 Routine Rapide (15 min)

### ⚡ Version Accélérée :
1. **Vérifications** : 3 min (matériel + paramètres)
2. **aim_botz** : 5 min (headshots + spray)
3. **Deathmatch** : 5 min (combat réel)
4. **Mental** : 2 min (respiration + objectifs)

### 🎯 Cas d'Urgence (5 min) :
- **Paramètres** : Vérification rapide
- **aim_botz** : 2 min de headshots
- **Respiration** : 1 min de relaxation
- **Go !** : Prêt à jouer

## 🎯 Checklist Pré-Match

### ✅ Technique :
- [ ] Souris nettoyée et fonctionnelle
- [ ] Sensibilité vérifiée
- [ ] Crosshair configuré
- [ ] Audio testé
- [ ] FPS stables
- [ ] Ping acceptable

### ✅ Physique :
- [ ] Position assise confortable
- [ ] Hydratation (bouteille d'eau)
- [ ] Température de la pièce
- [ ] Éclairage adapté
- [ ] Distractions éliminées

### ✅ Mental :
- [ ] Objectifs fixés
- [ ] État d'esprit positif
- [ ] Stress géré
- [ ] Concentration au maximum
- [ ] Motivation élevée

## 🎮 Préparation Environnementale

### 🏠 Espace de Jeu :
- **Rangement** : Espace propre et organisé
- **Température** : Ni trop chaud, ni trop froid
- **Éclairage** : Évite les reflets sur l'écran
- **Bruit** : Environnement calme
- **Distractions** : Téléphone en silence

### 🎯 Confort Physique :
- **Chaise** : Hauteur et support appropriés
- **Position** : Dos droit, pieds au sol
- **Distances** : Écran à bonne distance
- **Repos** : Évite la fatigue préalable

## 🎯 Préparation Mentale Avancée

### 🧠 Visualisation :
1. **Imagine** : Toi en train de bien jouer
2. **Détails** : Précision, communication, victoire
3. **Émotions** : Ressens la confiance
4. **Répète** : Plusieurs scénarios positifs

### 🎮 Objectifs SMART :
- **Spécifique** : "Améliorer ma précision"
- **Mesurable** : "80% de headshots"
- **Atteignable** : Réaliste pour ton niveau
- **Relevant** : Important pour ton jeu
- **Temporel** : Pour ce match

### 🎪 Motivation :
- **Pourquoi** : Tu joues à CS2
- **Plaisir** : Rappelle-toi que c'est un jeu
- **Progrès** : Pense à tes améliorations
- **Équipe** : Joue pour tes coéquipiers

## 🎯 Routines Spécifiques

### 🏆 Match Compétitif :
- **Temps** : 30 minutes de préparation
- **Échauffement** : Complet et varié
- **Mental** : Préparation approfondie
- **Vérifications** : Tout doit être parfait

### 🎮 Match Casual :
- **Temps** : 15 minutes suffisent
- **Échauffement** : Basique mais efficace
- **Mental** : Détendu mais concentré
- **Vérifications** : Essentielles seulement

### 🎯 Tournoi :
- **Temps** : 45 minutes minimum
- **Échauffement** : Très complet
- **Mental** : Préparation maximale
- **Vérifications** : Triple vérification

## 💡 Conseils Pratiques

### 🎮 Personnalisation :
- **Adapte** : Selon tes besoins
- **Teste** : Différentes routines
- **Garde** : Ce qui marche pour toi
- **Évolue** : Améliore avec l'expérience

### 🎯 Consistency :
- **Régularité** : Même routine à chaque fois
- **Timing** : Même durée
- **Ordre** : Même séquence
- **Habitude** : Jusqu'à ce que ça devienne naturel

## 🏆 Objectif Final

Une **bonne routine pré-match** peut améliorer tes performances de 15-20% ! C'est ce qui différencie les joueurs occasionnels des joueurs sérieux.

**Félicitations** : Tu as maintenant toutes les bases pour bien débuter CS2 !
`,
    tips: [
      'Crée une routine et respecte-la à chaque fois - la consistance est clé',
      'Adapte ta routine selon le temps disponible - 5, 15 ou 30 minutes',
      'Vérifie toujours tes paramètres - ils peuvent changer sans raison',
      'Prends le temps de te préparer mentalement - c\'est aussi important que l\'aim',
      'Reste flexible - ajuste ta routine selon ce qui marche pour toi'
    ],
    links: [
      { name: '🎯 Routines des pros', url: 'https://www.youtube.com/watch?v=pro-routines-cs2' },
      { name: '⚙️ Checklist configuration', url: 'https://prosettings.net/cs2/' },
      { name: '🎮 Discord Oupafamilly', url: 'https://discord.gg/oupafamilly' }
    ]
  }

  // Maintenant nous avons les 15 tutoriels débutants complets !
};