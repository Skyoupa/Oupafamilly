<?php
/**
 * API principale Oupafamilly - Migration FastAPI vers PHP
 * Point d'entrée pour toutes les routes API
 */

// Configuration des headers CORS
header('Content-Type: application/json; charset=utf-8');

// Gestion CORS pour les requêtes depuis React
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowedOrigins = [
    'http://localhost:3000',
    'https://your-ovh-domain.com' // Remplacer par votre domaine
];

if (in_array($origin, $allowedOrigins)) {
    header("Access-Control-Allow-Origin: $origin");
}

header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
header('Access-Control-Allow-Credentials: true');

// Gérer les requêtes OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Configuration PHP
ini_set('default_charset', 'utf-8');
mb_internal_encoding('UTF-8');

// Chargement des dépendances
require_once 'config.php';
require_once 'database.php';
require_once 'auth.php';

// Gestion des erreurs
set_error_handler(function($severity, $message, $file, $line) {
    if (DEBUG_MODE) {
        ApiResponse::error("PHP Error: $message in $file:$line", 500);
    } else {
        ApiResponse::serverError();
    }
    exit;
});

set_exception_handler(function($exception) {
    if (DEBUG_MODE) {
        ApiResponse::error("Exception: " . $exception->getMessage(), 500);
    } else {
        ApiResponse::serverError();
    }
    exit;
});

// Routeur simple
class Router {
    private $routes = [];
    
    public function addRoute($method, $pattern, $handler) {
        $this->routes[] = [
            'method' => strtoupper($method),
            'pattern' => $pattern,
            'handler' => $handler
        ];
    }
    
    public function get($pattern, $handler) {
        $this->addRoute('GET', $pattern, $handler);
    }
    
    public function post($pattern, $handler) {
        $this->addRoute('POST', $pattern, $handler);
    }
    
    public function put($pattern, $handler) {
        $this->addRoute('PUT', $pattern, $handler);
    }
    
    public function delete($pattern, $handler) {
        $this->addRoute('DELETE', $pattern, $handler);
    }
    
    public function dispatch() {
        $method = $_SERVER['REQUEST_METHOD'];
        $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
        
        // Supprimer le préfixe /api s'il existe
        $path = preg_replace('#^/api#', '', $path);
        
        foreach ($this->routes as $route) {
            if ($route['method'] === $method && preg_match('#^' . $route['pattern'] . '$#', $path, $matches)) {
                // Supprimer le premier élément (match complet)
                array_shift($matches);
                call_user_func_array($route['handler'], $matches);
                return;
            }
        }
        
        // Route non trouvée
        ApiResponse::notFound('API endpoint not found');
    }
}

// Initialisation
$router = new Router();

// Créer l'admin par défaut si nécessaire
Auth::createDefaultAdmin();

// ================================
// ROUTES AUTHENTIFICATION
// ================================

// POST /auth/register
$router->post('/auth/register', function() {
    try {
        $input = json_decode(file_get_contents('php://input'), true);
        
        Validator::required($input['username'] ?? '', 'username');
        Validator::required($input['email'] ?? '', 'email');
        Validator::required($input['password'] ?? '', 'password');
        
        Validator::username($input['username']);
        Validator::email($input['email']);
        Validator::password($input['password']);
        
        global $db;
        
        // Vérifier si l'utilisateur existe déjà
        $existing = $db->fetch(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            [$input['username'], $input['email']]
        );
        
        if ($existing) {
            ApiResponse::error('Username or email already exists', 400);
            return;
        }
        
        // Créer l'utilisateur
        $userId = Auth::generateUUID();
        $profileId = Auth::generateUUID();
        
        $db->beginTransaction();
        
        // Insérer l'utilisateur
        $db->query(
            "INSERT INTO users (id, username, email, hashed_password, role, status, is_verified, created_at) 
             VALUES (?, ?, ?, ?, 'member', 'active', 1, NOW())",
            [
                $userId,
                $input['username'],
                $input['email'],
                Auth::hashPassword($input['password'])
            ]
        );
        
        // Insérer le profil
        $db->query(
            "INSERT INTO user_profiles (id, user_id, display_name, coins, created_at) 
             VALUES (?, ?, ?, ?, NOW())",
            [
                $profileId,
                $userId,
                $input['username'],
                DEFAULT_COINS
            ]
        );
        
        $db->commit();
        
        // Créer le token
        $token = Auth::createJWT($userId, $input['username'], $input['email'], 'member');
        
        ApiResponse::success([
            'access_token' => $token,
            'token_type' => 'bearer',
            'user' => [
                'id' => $userId,
                'username' => $input['username'],
                'email' => $input['email'],
                'role' => 'member'
            ]
        ]);
        
    } catch (Exception $e) {
        if (isset($db)) $db->rollback();
        ApiResponse::error($e->getMessage(), 400);
    }
});

// POST /auth/login
$router->post('/auth/login', function() {
    try {
        $input = json_decode(file_get_contents('php://input'), true);
        
        Validator::required($input['username'] ?? '', 'username');
        Validator::required($input['password'] ?? '', 'password');
        
        global $db;
        
        // Trouver l'utilisateur (par username ou email)
        $user = $db->fetch(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            [$input['username'], $input['username']]
        );
        
        if (!$user || !Auth::verifyPassword($input['password'], $user['hashed_password'])) {
            ApiResponse::error('Invalid credentials', 401);
            return;
        }
        
        if ($user['status'] !== 'active') {
            ApiResponse::error('Account is not active', 401);
            return;
        }
        
        // Mettre à jour la dernière connexion
        $db->query(
            "UPDATE users SET last_login = NOW() WHERE id = ?",
            [$user['id']]
        );
        
        // Créer le token
        $token = Auth::createJWT($user['id'], $user['username'], $user['email'], $user['role']);
        
        ApiResponse::success([
            'access_token' => $token,
            'token_type' => 'bearer',
            'user' => [
                'id' => $user['id'],
                'username' => $user['username'],
                'email' => $user['email'],
                'role' => $user['role']
            ]
        ]);
        
    } catch (Exception $e) {
        ApiResponse::error($e->getMessage(), 400);
    }
});

// GET /auth/me
$router->get('/auth/me', function() {
    $user = Auth::requireAuth();
    
    ApiResponse::success([
        'id' => $user['id'],
        'username' => $user['username'],
        'email' => $user['email'],
        'role' => $user['role'],
        'profile' => [
            'display_name' => $user['display_name'],
            'bio' => $user['bio'],
            'coins' => (int)$user['coins'],
            'level' => (int)$user['level'],
            'elo_rating' => (int)$user['elo_rating']
        ]
    ]);
});

// ================================
// ROUTES UTILISATEURS
// ================================

// GET /users
$router->get('/users', function() {
    global $db;
    
    $page = (int)($_GET['page'] ?? 1);
    $limit = min((int)($_GET['limit'] ?? 20), 100);
    $offset = ($page - 1) * $limit;
    
    $users = $db->fetchAll(
        "SELECT u.id, u.username, u.email, u.role, u.status, u.created_at,
                up.display_name, up.coins, up.level, up.elo_rating, up.total_tournaments
         FROM users u
         LEFT JOIN user_profiles up ON u.id = up.user_id
         ORDER BY u.created_at DESC
         LIMIT ? OFFSET ?",
        [$limit, $offset]
    );
    
    $total = $db->fetch("SELECT COUNT(*) as count FROM users")['count'];
    
    ApiResponse::success([
        'users' => $users,
        'total' => (int)$total,
        'page' => $page,
        'pages' => ceil($total / $limit)
    ]);
});

// GET /users/{id}
$router->get('/users/([a-f0-9-]+)', function($userId) {
    global $db;
    
    $user = $db->fetch(
        "SELECT u.*, up.* FROM users u
         LEFT JOIN user_profiles up ON u.id = up.user_id
         WHERE u.id = ?",
        [$userId]
    );
    
    if (!$user) {
        ApiResponse::notFound('User not found');
        return;
    }
    
    // Ne pas retourner le hash du mot de passe
    unset($user['hashed_password']);
    
    ApiResponse::success($user);
});

// ================================
// ROUTES TOURNOIS
// ================================

// GET /tournaments/
$router->get('/tournaments/?', function() {
    global $db;
    
    $status = $_GET['status'] ?? null;
    $game = $_GET['game'] ?? null;
    $limit = min((int)($_GET['limit'] ?? 20), 100);
    
    $where = [];
    $params = [];
    
    if ($status) {
        $where[] = "status = ?";
        $params[] = $status;
    }
    
    if ($game) {
        $where[] = "game = ?";
        $params[] = $game;
    }
    
    $whereClause = $where ? "WHERE " . implode(" AND ", $where) : "";
    
    $tournaments = $db->fetchAll(
        "SELECT t.*, u.username as created_by_username
         FROM tournaments t
         LEFT JOIN users u ON t.created_by = u.id
         $whereClause
         ORDER BY t.start_date DESC
         LIMIT ?",
        array_merge($params, [$limit])
    );
    
    // Décoder les JSON
    foreach ($tournaments as &$tournament) {
        $tournament['participants'] = json_decode($tournament['participants'] ?? '[]', true);
        $tournament['brackets'] = json_decode($tournament['brackets'] ?? '[]', true);
        $tournament['matches'] = json_decode($tournament['matches'] ?? '[]', true);
    }
    
    ApiResponse::success($tournaments);
});

// POST /tournaments/{id}/register
$router->post('/tournaments/([a-f0-9-]+)/register', function($tournamentId) {
    $user = Auth::requireAuth();
    global $db;
    
    try {
        $tournament = $db->fetch("SELECT * FROM tournaments WHERE id = ?", [$tournamentId]);
        
        if (!$tournament) {
            ApiResponse::notFound('Tournament not found');
            return;
        }
        
        if ($tournament['status'] !== 'open') {
            ApiResponse::error('Tournament is not open for registration', 400);
            return;
        }
        
        $participants = json_decode($tournament['participants'] ?? '[]', true);
        
        if (in_array($user['id'], $participants)) {
            ApiResponse::error('Already registered for this tournament', 400);
            return;
        }
        
        if (count($participants) >= $tournament['max_participants']) {
            ApiResponse::error('Tournament is full', 400);
            return;
        }
        
        $participants[] = $user['id'];
        
        $db->query(
            "UPDATE tournaments SET participants = ? WHERE id = ?",
            [json_encode($participants), $tournamentId]
        );
        
        ApiResponse::success(['message' => 'Successfully registered for tournament']);
        
    } catch (Exception $e) {
        ApiResponse::error($e->getMessage(), 400);
    }
});

// ================================
// ROUTES ÉCONOMIE
// ================================

// GET /currency/balance
$router->get('/currency/balance', function() {
    $user = Auth::requireAuth();
    
    ApiResponse::success([
        'balance' => (int)$user['coins'],
        'total_earned' => (int)$user['total_coins_earned']
    ]);
});

// GET /currency/marketplace
$router->get('/currency/marketplace', function() {
    global $db;
    
    $items = $db->fetchAll(
        "SELECT * FROM marketplace_items WHERE is_available = 1 ORDER BY price ASC"
    );
    
    ApiResponse::success($items);
});

// ================================
// ROUTES COMMUNAUTÉ
// ================================

// GET /community/members
$router->get('/community/members', function() {
    global $db;
    
    $members = $db->fetchAll(
        "SELECT u.id, u.username, u.role, u.created_at,
                up.display_name, up.level, up.elo_rating, up.total_tournaments
         FROM users u
         LEFT JOIN user_profiles up ON u.id = up.user_id
         WHERE u.status = 'active'
         ORDER BY up.level DESC, up.elo_rating DESC
         LIMIT 50"
    );
    
    ApiResponse::success($members);
});

// GET /community/stats
$router->get('/community/stats', function() {
    global $db;
    
    $stats = [
        'total_members' => (int)$db->fetch("SELECT COUNT(*) as count FROM users WHERE status = 'active'")['count'],
        'total_tournaments' => (int)$db->fetch("SELECT COUNT(*) as count FROM tournaments")['count'],
        'active_tournaments' => (int)$db->fetch("SELECT COUNT(*) as count FROM tournaments WHERE status IN ('open', 'in_progress')")['count'],
        'total_matches' => (int)$db->fetch("SELECT COUNT(*) as count FROM matches")['count']
    ];
    
    ApiResponse::success($stats);
});

// ================================
// ROUTES ÉQUIPES
// ================================

// GET /teams/my-teams
$router->get('/teams/my-teams', function() {
    $user = Auth::requireAuth();
    global $db;
    
    $teams = $db->fetchAll(
        "SELECT * FROM teams 
         WHERE captain_id = ? OR JSON_CONTAINS(members, ?)",
        [$user['id'], '"' . $user['id'] . '"']
    );
    
    foreach ($teams as &$team) {
        $team['members'] = json_decode($team['members'] ?? '[]', true);
        $team['is_captain'] = $team['captain_id'] === $user['id'];
    }
    
    ApiResponse::success(['teams' => $teams]);
});

// POST /teams/create
$router->post('/teams/create', function() {
    $user = Auth::requireAuth();
    global $db;
    
    try {
        $input = json_decode(file_get_contents('php://input'), true);
        
        Validator::required($input['name'] ?? '', 'name');
        Validator::required($input['game'] ?? '', 'game');
        Validator::inArray($input['game'], SUPPORTED_GAMES, 'game');
        
        $teamId = Auth::generateUUID();
        
        $db->query(
            "INSERT INTO teams (id, name, game, description, captain_id, members, max_members, is_open, created_at)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())",
            [
                $teamId,
                $input['name'],
                $input['game'],
                $input['description'] ?? '',
                $user['id'],
                json_encode([$user['id']]),
                $input['max_members'] ?? 5,
                $input['is_open'] ?? true
            ]
        );
        
        ApiResponse::success(['message' => 'Team created successfully', 'team_id' => $teamId]);
        
    } catch (Exception $e) {
        ApiResponse::error($e->getMessage(), 400);
    }
});

// ================================
// ROUTES ADMIN (Analytics Overview)
// ================================

// GET /analytics/overview
$router->get('/analytics/overview', function() {
    $admin = Auth::requireAdmin();
    global $db;
    
    try {
        // Statistiques générales
        $overview = [
            'total_users' => (int)$db->fetch("SELECT COUNT(*) as count FROM users")['count'],
            'active_users' => (int)$db->fetch("SELECT COUNT(*) as count FROM users WHERE status = 'active'")['count'],
            'total_tournaments' => (int)$db->fetch("SELECT COUNT(*) as count FROM tournaments")['count'],
            'active_tournaments' => (int)$db->fetch("SELECT COUNT(*) as count FROM tournaments WHERE status IN ('open', 'in_progress')")['count'],
            'total_teams' => (int)$db->fetch("SELECT COUNT(*) as count FROM teams")['count'],
            'total_coins' => (int)$db->fetch("SELECT SUM(coins) as total FROM user_profiles")['total'],
            'marketplace_items' => (int)$db->fetch("SELECT COUNT(*) as count FROM marketplace_items WHERE is_available = 1")['count']
        ];
        
        // Engagement utilisateurs
        $user_engagement = [
            'new_users_today' => (int)$db->fetch("SELECT COUNT(*) as count FROM users WHERE DATE(created_at) = CURDATE()")['count'],
            'active_users_week' => (int)$db->fetch("SELECT COUNT(*) as count FROM users WHERE last_login >= DATE_SUB(NOW(), INTERVAL 7 DAY)")['count'],
            'avg_session_time' => 1200 // Mock data
        ];
        
        // Activité gaming
        $gaming_activity = [
            'matches_today' => (int)$db->fetch("SELECT COUNT(*) as count FROM matches WHERE DATE(created_at) = CURDATE()")['count'],
            'tournaments_this_month' => (int)$db->fetch("SELECT COUNT(*) as count FROM tournaments WHERE MONTH(created_at) = MONTH(NOW())")['count'],
            'top_game' => 'cs2'
        ];
        
        // Économie
        $economy = [
            'total_circulation' => (int)$db->fetch("SELECT SUM(coins) as total FROM user_profiles")['total'],
            'avg_balance' => (int)$db->fetch("SELECT AVG(coins) as avg FROM user_profiles")['avg'],
            'transactions_today' => (int)$db->fetch("SELECT COUNT(*) as count FROM currency_transactions WHERE DATE(created_at) = CURDATE()")['count']
        ];
        
        // Achievements
        $achievements = [
            'total_achievements' => (int)$db->fetch("SELECT COUNT(*) as count FROM achievements")['count'],
            'achievements_earned' => (int)$db->fetch("SELECT COUNT(*) as count FROM user_achievements")['count'],
            'top_achievement' => 'première_connexion'
        ];
        
        // Stats en temps réel
        $realtime = [
            'online_users' => rand(15, 25), // Mock data
            'active_matches' => (int)$db->fetch("SELECT COUNT(*) as count FROM matches WHERE status = 'in_progress'")['count'],
            'server_status' => 'healthy'
        ];
        
        // Performance
        $performance = [
            'response_time' => rand(80, 120) . 'ms',
            'uptime' => '99.9%',
            'last_updated' => date('c')
        ];
        
        ApiResponse::success([
            'overview' => $overview,
            'user_engagement' => $user_engagement,
            'gaming_activity' => $gaming_activity,
            'economy' => $economy,
            'achievements' => $achievements,
            'realtime' => $realtime,
            'performance' => $performance
        ]);
        
    } catch (Exception $e) {
        ApiResponse::error('Error generating analytics: ' . $e->getMessage(), 500);
    }
});

// ================================
// ROUTES CONTENU
// ================================

// GET /content/tutorials
$router->get('/content/tutorials', function() {
    // Retourner les tutoriels (simulés pour la migration)
    $tutorials = [];
    
    // Tutoriels CS2 de base
    $cs2Tutorials = [
        [
            'id' => '1',
            'title' => 'Utilisation des grenades de base',
            'description' => 'Apprenez à utiliser efficacement les grenades dans CS2',
            'game' => 'cs2',
            'gameId' => 'cs2',
            'level' => 'Débutant',
            'levelOriginal' => 'beginner',
            'levelDisplay' => 'Débutant',
            'image' => '/images/tutorials/grenades.jpg',
            'published' => true,
            'sort_order' => 1
        ],
        [
            'id' => '2', 
            'title' => 'Positionnement sur Dust2',
            'description' => 'Maîtrisez les positions clés sur la carte Dust2',
            'game' => 'cs2',
            'gameId' => 'cs2',
            'level' => 'Intermédiaire',
            'levelOriginal' => 'intermediate',
            'levelDisplay' => 'Intermédiaire',
            'image' => '/images/tutorials/dust2.jpg',
            'published' => true,
            'sort_order' => 2
        ],
        [
            'id' => '3',
            'title' => 'Techniques de visée avancées',
            'description' => 'Perfectionnez votre aim avec des techniques pro',
            'game' => 'cs2',
            'gameId' => 'cs2', 
            'level' => 'Expert',
            'levelOriginal' => 'expert',
            'levelDisplay' => 'Expert',
            'image' => '/images/tutorials/aim.jpg',
            'published' => true,
            'sort_order' => 3
        ]
    ];
    
    $game = $_GET['game'] ?? null;
    $limit = min((int)($_GET['limit'] ?? 100), 100);
    
    if ($game === 'cs2' || !$game) {
        $tutorials = array_slice($cs2Tutorials, 0, $limit);
    }
    
    ApiResponse::success($tutorials);
});

// ================================
// ROUTE PAR DÉFAUT
// ================================

// GET / (status check)
$router->get('/?', function() {
    ApiResponse::success([
        'status' => 'ok',
        'service' => 'Oupafamilly API',
        'version' => '1.0.0-php',
        'timestamp' => date('c')
    ]);
});

// Démarrer le routeur
$router->dispatch();
?>