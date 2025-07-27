<?php
/**
 * Configuration de la base de données MySQL OVH
 * pour la migration Oupafamilly
 */

// Configuration MySQL OVH
define('DB_HOST', 'oupafaj803.mysql.db');  // Essayez aussi mysql10-68.perso.sfr.sh si ça ne marche pas
define('DB_NAME', 'oupafaj803');
define('DB_USER', 'oupafaj803');
define('DB_PASS', 'e6f3R9s3N6dYwjqU');
define('DB_CHARSET', 'utf8mb4');

// Configuration CORS pour React frontend
define('ALLOWED_ORIGINS', [
    'http://localhost:3000',
    'https://your-ovh-domain.com'  // Remplacer par votre domaine OVH
]);

// Configuration JWT (même secret que FastAPI)
define('JWT_SECRET', 'your-super-secret-jwt-key-here');
define('JWT_EXPIRE_HOURS', 24);

// Configuration générale
define('TIMEZONE', 'Europe/Paris');
define('DEBUG_MODE', true);  // Mettre à false en production

// Configuration des uploads
define('UPLOAD_MAX_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_IMAGES', ['jpg', 'jpeg', 'png', 'gif']);

// Configuration des limitations
define('RATE_LIMIT_REQUESTS', 100);
define('RATE_LIMIT_WINDOW', 3600); // 1 heure

// Configuration Redis (si nécessaire - peut être désactivé sur OVH)
define('REDIS_ENABLED', false);
define('REDIS_HOST', 'localhost');
define('REDIS_PORT', 6379);

// Configuration des logs
define('LOG_LEVEL', 'INFO');
define('LOG_FILE', __DIR__ . '/logs/app.log');

// Configuration des jeux supportés
define('SUPPORTED_GAMES', ['cs2', 'lol', 'wow', 'sc2', 'minecraft']);

// Configuration des rôles utilisateurs
define('USER_ROLES', ['admin', 'moderator', 'member']);
define('USER_STATUSES', ['active', 'inactive', 'pending']);

// Configuration des tournois
define('TOURNAMENT_STATUSES', ['draft', 'open', 'in_progress', 'completed', 'cancelled']);
define('TOURNAMENT_TYPES', ['elimination', 'bracket', 'round_robin']);

// Configuration par défaut pour les nouveaux utilisateurs
define('DEFAULT_COINS', 100);
define('DEFAULT_ELO', 1200);
define('DEFAULT_LEVEL', 1);

// Configuration email (pour OVH mail)
define('MAIL_HOST', 'ssl0.ovh.net');
define('MAIL_PORT', 587);
define('MAIL_USERNAME', 'contact@oupafamilly.com');
define('MAIL_PASSWORD', ''); // À configurer
define('MAIL_FROM', 'contact@oupafamilly.com');
define('MAIL_FROM_NAME', 'Oupafamilly');

// Définir le fuseau horaire
date_default_timezone_set(TIMEZONE);

// Configuration de l'affichage des erreurs
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(E_ERROR | E_WARNING | E_PARSE);
    ini_set('display_errors', 0);
}
?>