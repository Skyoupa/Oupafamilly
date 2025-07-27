<?php
/**
 * Configuration de la base de données MySQL OVH
 * pour la migration Oupafamilly - VERSION PRODUCTION
 */

// Configuration MySQL OVH - PRODUCTION
define('DB_HOST', 'oupafaj803.mysql.db');
define('DB_NAME', 'oupafaj803');
define('DB_USER', 'oupafaj803');
define('DB_PASS', 'e6f3R9s3N6dYwjqU');
define('DB_CHARSET', 'utf8mb4');

// Configuration CORS pour React frontend - PRODUCTION
define('ALLOWED_ORIGINS', [
    'https://oupafamilly.com',
    'https://www.oupafamilly.com',
    'http://localhost:3000'  // Pour les tests locaux
]);

// Configuration JWT - CHANGER EN PRODUCTION
define('JWT_SECRET', 'CHANGEZ-CETTE-CLE-EN-PRODUCTION-POUR-PLUS-DE-SECURITE');
define('JWT_EXPIRE_HOURS', 24);

// Configuration générale - PRODUCTION
define('TIMEZONE', 'Europe/Paris');
define('DEBUG_MODE', false);  // ⚠️ DÉSACTIVÉ EN PRODUCTION

// Configuration des uploads
define('UPLOAD_MAX_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_IMAGES', ['jpg', 'jpeg', 'png', 'gif']);

// Configuration des limitations
define('RATE_LIMIT_REQUESTS', 100);
define('RATE_LIMIT_WINDOW', 3600); // 1 heure

// Configuration Redis (désactivé sur hébergement mutualisé OVH)
define('REDIS_ENABLED', false);

// Configuration des logs
define('LOG_LEVEL', 'ERROR'); // Seulement les erreurs en production
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

// Configuration email OVH
define('MAIL_HOST', 'ssl0.ovh.net');
define('MAIL_PORT', 587);
define('MAIL_USERNAME', 'contact@oupafamilly.com');
define('MAIL_PASSWORD', ''); // ⚠️ À CONFIGURER
define('MAIL_FROM', 'contact@oupafamilly.com');
define('MAIL_FROM_NAME', 'Oupafamilly');

// Définir le fuseau horaire
date_default_timezone_set(TIMEZONE);

// Configuration de l'affichage des erreurs PRODUCTION
error_reporting(E_ERROR | E_WARNING | E_PARSE);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/logs/php_errors.log');

// Créer le dossier de logs s'il n'existe pas
if (!is_dir(__DIR__ . '/logs')) {
    mkdir(__DIR__ . '/logs', 0755, true);
}
?>