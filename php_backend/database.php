<?php
/**
 * Base de données MySQL - Classe de connexion et gestion
 * Migration de MongoDB vers MySQL pour Oupafamilly
 */

require_once 'config.php';

class Database {
    private static $instance = null;
    private $connection;
    
    private function __construct() {
        try {
            $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES " . DB_CHARSET
            ];
            
            $this->connection = new PDO($dsn, DB_USER, DB_PASS, $options);
            
            // Créer les tables si elles n'existent pas
            $this->createTables();
            
        } catch (PDOException $e) {
            error_log("Erreur de connexion à la base de données: " . $e->getMessage());
            throw new Exception("Impossible de se connecter à la base de données");
        }
    }
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    public function getConnection() {
        return $this->connection;
    }
    
    /**
     * Créer toutes les tables nécessaires pour Oupafamilly
     */
    private function createTables() {
        $queries = [
            // Table users (équivalent User model)
            "CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'moderator', 'member') DEFAULT 'member',
                status ENUM('active', 'inactive', 'pending') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_verified BOOLEAN DEFAULT FALSE,
                INDEX idx_username (username),
                INDEX idx_email (email),
                INDEX idx_role (role)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table user_profiles (équivalent UserProfile model)
            "CREATE TABLE IF NOT EXISTS user_profiles (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                display_name VARCHAR(100) NOT NULL,
                bio TEXT,
                avatar_url LONGTEXT,
                banner_url LONGTEXT,
                location VARCHAR(100),
                favorite_games JSON,
                gaming_experience JSON,
                discord_username VARCHAR(50),
                twitch_username VARCHAR(50),
                steam_profile VARCHAR(100),
                total_tournaments INT DEFAULT 0,
                tournaments_won INT DEFAULT 0,
                trophies_1v1 INT DEFAULT 0,
                trophies_2v2 INT DEFAULT 0,
                trophies_5v5 INT DEFAULT 0,
                total_points INT DEFAULT 0,
                coins INT DEFAULT 100,
                total_coins_earned INT DEFAULT 100,
                experience_points INT DEFAULT 0,
                level INT DEFAULT 1,
                elo_rating INT DEFAULT 1200,
                peak_elo INT DEFAULT 1200,
                elo_history JSON,
                seasonal_elo JSON,
                current_season VARCHAR(20) DEFAULT '2025-S1',
                badges JSON,
                achievements JSON,
                comments_received INT DEFAULT 0,
                average_rating DECIMAL(3,2) DEFAULT 0.00,
                total_ratings INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_elo (elo_rating),
                INDEX idx_level (level)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table tournaments
            "CREATE TABLE IF NOT EXISTS tournaments (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                game ENUM('cs2', 'lol', 'wow', 'sc2', 'minecraft') NOT NULL,
                tournament_type ENUM('elimination', 'bracket', 'round_robin') NOT NULL,
                status ENUM('draft', 'open', 'in_progress', 'completed', 'cancelled') DEFAULT 'draft',
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                max_participants INT DEFAULT 32,
                entry_fee INT DEFAULT 0,
                prize_pool INT DEFAULT 0,
                rules TEXT,
                participants JSON,
                brackets JSON,
                matches JSON,
                created_by VARCHAR(36) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id),
                INDEX idx_game (game),
                INDEX idx_status (status),
                INDEX idx_start_date (start_date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table teams
            "CREATE TABLE IF NOT EXISTS teams (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                game ENUM('cs2', 'lol', 'wow', 'sc2', 'minecraft') NOT NULL,
                description TEXT,
                captain_id VARCHAR(36) NOT NULL,
                members JSON,
                max_members INT DEFAULT 5,
                is_open BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (captain_id) REFERENCES users(id),
                INDEX idx_game (game),
                INDEX idx_captain (captain_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table matches
            "CREATE TABLE IF NOT EXISTS matches (
                id VARCHAR(36) PRIMARY KEY,
                tournament_id VARCHAR(36) NOT NULL,
                round_number INT NOT NULL,
                match_number INT NOT NULL,
                player1_id VARCHAR(36),
                player2_id VARCHAR(36),
                team1_id VARCHAR(36),
                team2_id VARCHAR(36),
                status ENUM('scheduled', 'in_progress', 'completed', 'cancelled') DEFAULT 'scheduled',
                scheduled_at TIMESTAMP,
                started_at TIMESTAMP NULL,
                completed_at TIMESTAMP NULL,
                result JSON,
                score JSON,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(id) ON DELETE CASCADE,
                INDEX idx_tournament (tournament_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table news
            "CREATE TABLE IF NOT EXISTS news (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content LONGTEXT NOT NULL,
                summary TEXT,
                author_id VARCHAR(36) NOT NULL,
                is_published BOOLEAN DEFAULT FALSE,
                is_pinned BOOLEAN DEFAULT FALSE,
                tags JSON,
                views INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id),
                INDEX idx_published (is_published),
                INDEX idx_pinned (is_pinned),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table comments
            "CREATE TABLE IF NOT EXISTS comments (
                id VARCHAR(36) PRIMARY KEY,
                target_type ENUM('profile', 'tournament', 'news') NOT NULL,
                target_id VARCHAR(36) NOT NULL,
                author_id VARCHAR(36) NOT NULL,
                content TEXT NOT NULL,
                rating INT DEFAULT NULL,
                is_approved BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id),
                INDEX idx_target (target_type, target_id),
                INDEX idx_author (author_id),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table chat_messages
            "CREATE TABLE IF NOT EXISTS chat_messages (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                username VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_system BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                INDEX idx_user (user_id),
                INDEX idx_timestamp (timestamp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table currency_transactions
            "CREATE TABLE IF NOT EXISTS currency_transactions (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                amount INT NOT NULL,
                transaction_type ENUM('earn', 'spend', 'admin_adjust') NOT NULL,
                source VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                INDEX idx_user (user_id),
                INDEX idx_type (transaction_type),
                INDEX idx_created (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table achievements
            "CREATE TABLE IF NOT EXISTS achievements (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                badge_emoji VARCHAR(10) NOT NULL,
                category VARCHAR(50) NOT NULL,
                rarity ENUM('common', 'rare', 'epic', 'legendary', 'mythic') DEFAULT 'common',
                points INT DEFAULT 0,
                requirements JSON,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table user_achievements (relation many-to-many)
            "CREATE TABLE IF NOT EXISTS user_achievements (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                achievement_id VARCHAR(36) NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_achievement (user_id, achievement_id),
                INDEX idx_user (user_id),
                INDEX idx_achievement (achievement_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table daily_quests
            "CREATE TABLE IF NOT EXISTS daily_quests (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                quest_type VARCHAR(50) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                target_value INT NOT NULL,
                current_progress INT DEFAULT 0,
                reward_coins INT DEFAULT 0,
                reward_xp INT DEFAULT 0,
                is_completed BOOLEAN DEFAULT FALSE,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user (user_id),
                INDEX idx_completed (is_completed),
                INDEX idx_expires (expires_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table marketplace_items
            "CREATE TABLE IF NOT EXISTS marketplace_items (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                price INT NOT NULL,
                item_type VARCHAR(50) NOT NULL,
                rarity ENUM('common', 'rare', 'epic', 'legendary', 'mythic') DEFAULT 'common',
                is_available BOOLEAN DEFAULT TRUE,
                stock INT DEFAULT -1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_type (item_type),
                INDEX idx_available (is_available),
                INDEX idx_price (price)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
            
            // Table betting_markets
            "CREATE TABLE IF NOT EXISTS betting_markets (
                id VARCHAR(36) PRIMARY KEY,
                tournament_id VARCHAR(36) NOT NULL,
                match_id VARCHAR(36),
                title VARCHAR(200) NOT NULL,
                description TEXT,
                game VARCHAR(20) NOT NULL,
                status ENUM('open', 'locked', 'settled', 'cancelled') DEFAULT 'open',
                total_pool INT DEFAULT 0,
                outcome VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closes_at TIMESTAMP NOT NULL,
                settled_at TIMESTAMP NULL,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
                INDEX idx_tournament (tournament_id),
                INDEX idx_status (status),
                INDEX idx_game (game)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        ];
        
        foreach ($queries as $query) {
            try {
                $this->connection->exec($query);
            } catch (PDOException $e) {
                error_log("Erreur lors de la création de table: " . $e->getMessage());
                error_log("Query: " . $query);
            }
        }
        
        // Insérer les données par défaut
        $this->insertDefaultData();
    }
    
    /**
     * Insérer les données par défaut (achievements, marketplace items, etc.)
     */
    private function insertDefaultData() {
        // Insérer les achievements par défaut
        $this->insertDefaultAchievements();
        
        // Insérer les items marketplace par défaut
        $this->insertDefaultMarketplaceItems();
    }
    
    private function insertDefaultAchievements() {
        $achievements = [
            ['première_connexion', '🎯 Première Connexion', 'Se connecter pour la première fois', 'onboarding', 'common', 10],
            ['profil_complet', '✨ Profil Complet', 'Compléter son profil utilisateur', 'profile', 'common', 25],
            ['premier_commentaire', '💬 Premier Commentaire', 'Écrire son premier commentaire', 'social', 'common', 15],
            ['premier_tournoi', '🏆 Premier Tournoi', 'Participer à son premier tournoi', 'competition', 'rare', 50],
            ['victoire_tournoi', '🥇 Première Victoire', 'Remporter son premier tournoi', 'competition', 'epic', 100],
            ['collectionneur', '💎 Collectionneur', 'Obtenir 10 badges différents', 'collection', 'legendary', 200],
            ['chat_actif', '🗣️ Bavard', 'Envoyer 100 messages dans le chat', 'social', 'rare', 75],
            ['elo_master', '⚡ ELO Master', 'Atteindre 1800+ de rating ELO', 'skill', 'epic', 150],
            ['millionaire', '💰 Millionnaire', 'Accumuler 10000 coins', 'economy', 'legendary', 250],
            ['membre_élite', '👑 Membre Élite', 'Être membre depuis plus d\'un an', 'loyalty', 'mythic', 500]
        ];
        
        $stmt = $this->connection->prepare("
            INSERT IGNORE INTO achievements (id, name, description, badge_emoji, category, rarity, points)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($achievements as $achievement) {
            $id = $this->generateUUID();
            $stmt->execute([
                $id,
                $achievement[1], // title
                $achievement[2], // description  
                '🏆', // badge_emoji
                $achievement[3], // category
                $achievement[4], // rarity
                $achievement[5]  // points
            ]);
        }
    }
    
    private function insertDefaultMarketplaceItems() {
        $items = [
            ['Avatar Premium', 'Avatar personnalisé de haute qualité', 500, 'avatar', 'rare'],
            ['Bannière Elite', 'Bannière personnalisée pour votre profil', 750, 'banner', 'epic'],
            ['Badge Exclusif', 'Badge spécial visible sur votre profil', 1000, 'badge', 'legendary'],
            ['Boost XP x2', 'Double l\'XP gagné pendant 24h', 200, 'boost', 'common'],
            ['Titre Personnalisé', 'Titre unique affiché sous votre nom', 1500, 'title', 'mythic'],
            ['Emote Spécial', 'Emote exclusif pour le chat', 300, 'emote', 'rare'],
            ['Couleur Pseudo', 'Couleur personnalisée pour votre pseudo', 600, 'color', 'epic'],
            ['Pack Starter', 'Pack de démarrage avec bonus', 100, 'pack', 'common']
        ];
        
        $stmt = $this->connection->prepare("
            INSERT IGNORE INTO marketplace_items (id, name, description, price, item_type, rarity)
            VALUES (?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($items as $item) {
            $id = $this->generateUUID();
            $stmt->execute([
                $id,
                $item[0], // name
                $item[1], // description
                $item[2], // price
                $item[3], // item_type
                $item[4]  // rarity
            ]);
        }
    }
    
    /**
     * Générer un UUID v4
     */
    public function generateUUID() {
        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }
    
    /**
     * Exécuter une requête préparée
     */
    public function query($sql, $params = []) {
        try {
            $stmt = $this->connection->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch (PDOException $e) {
            error_log("Erreur requête SQL: " . $e->getMessage());
            error_log("SQL: " . $sql);
            throw $e;
        }
    }
    
    /**
     * Obtenir une ligne
     */
    public function fetch($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetch();
    }
    
    /**
     * Obtenir toutes les lignes
     */
    public function fetchAll($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $stmt->fetchAll();
    }
    
    /**
     * Insérer et retourner l'ID
     */
    public function insert($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        return $this->connection->lastInsertId();
    }
    
    /**
     * Commencer une transaction
     */
    public function beginTransaction() {
        return $this->connection->beginTransaction();
    }
    
    /**
     * Valider une transaction
     */
    public function commit() {
        return $this->connection->commit();
    }
    
    /**
     * Annuler une transaction
     */
    public function rollback() {
        return $this->connection->rollback();
    }
}

// Instance globale
$db = Database::getInstance();
?>