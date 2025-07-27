<?php
/**
 * Utilitaires pour l'authentification et la sécurité
 * Migration FastAPI Auth vers PHP
 */

require_once 'config.php';

class Auth {
    
    /**
     * Générer un hash du mot de passe (équivalent de get_password_hash)
     */
    public static function hashPassword($password) {
        return password_hash($password, PASSWORD_ARGON2ID, [
            'memory_cost' => 65536, // 64 MB
            'time_cost' => 4,       // 4 iterations
            'threads' => 3,         // 3 threads
        ]);
    }
    
    /**
     * Vérifier un mot de passe (équivalent de verify_password)
     */
    public static function verifyPassword($password, $hash) {
        return password_verify($password, $hash);
    }
    
    /**
     * Créer un token JWT
     */
    public static function createJWT($user_id, $username, $email, $role) {
        $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
        
        $payload = json_encode([
            'user_id' => $user_id,
            'username' => $username,
            'email' => $email,
            'role' => $role,
            'iat' => time(),
            'exp' => time() + (JWT_EXPIRE_HOURS * 3600)
        ]);
        
        $base64Header = self::base64UrlEncode($header);
        $base64Payload = self::base64UrlEncode($payload);
        
        $signature = hash_hmac('sha256', $base64Header . "." . $base64Payload, JWT_SECRET, true);
        $base64Signature = self::base64UrlEncode($signature);
        
        return $base64Header . "." . $base64Payload . "." . $base64Signature;
    }
    
    /**
     * Vérifier et décoder un token JWT
     */
    public static function verifyJWT($token) {
        $parts = explode(".", $token);
        if (count($parts) !== 3) {
            return false;
        }
        
        $header = self::base64UrlDecode($parts[0]);
        $payload = self::base64UrlDecode($parts[1]);
        $signature = self::base64UrlDecode($parts[2]);
        
        $expectedSignature = hash_hmac('sha256', $parts[0] . "." . $parts[1], JWT_SECRET, true);
        
        if (!hash_equals($signature, $expectedSignature)) {
            return false;
        }
        
        $payloadData = json_decode($payload, true);
        
        // Vérifier l'expiration
        if (isset($payloadData['exp']) && $payloadData['exp'] < time()) {
            return false;
        }
        
        return $payloadData;
    }
    
    /**
     * Obtenir l'utilisateur actuel depuis le token
     */
    public static function getCurrentUser() {
        $headers = getallheaders();
        $authHeader = $headers['Authorization'] ?? $headers['authorization'] ?? '';
        
        if (!$authHeader || !preg_match('/Bearer\s(\S+)/', $authHeader, $matches)) {
            return null;
        }
        
        $token = $matches[1];
        $payload = self::verifyJWT($token);
        
        if (!$payload) {
            return null;
        }
        
        global $db;
        $user = $db->fetch(
            "SELECT u.*, up.* FROM users u 
             LEFT JOIN user_profiles up ON u.id = up.user_id 
             WHERE u.id = ?", 
            [$payload['user_id']]
        );
        
        return $user;
    }
    
    /**
     * Vérifier si l'utilisateur est admin
     */
    public static function requireAdmin() {
        $user = self::getCurrentUser();
        if (!$user || $user['role'] !== 'admin') {
            http_response_code(403);
            echo json_encode(['error' => 'Access denied. Admin required.']);
            exit;
        }
        return $user;
    }
    
    /**
     * Vérifier si l'utilisateur est connecté
     */
    public static function requireAuth() {
        $user = self::getCurrentUser();
        if (!$user) {
            http_response_code(401);
            echo json_encode(['error' => 'Authentication required']);
            exit;
        }
        return $user;
    }
    
    /**
     * Encoder en base64 URL-safe
     */
    private static function base64UrlEncode($data) {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }
    
    /**
     * Décoder depuis base64 URL-safe
     */
    private static function base64UrlDecode($data) {
        return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '='));
    }
    
    /**
     * Générer un UUID v4
     */
    public static function generateUUID() {
        return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff), mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
        );
    }
    
    /**
     * Valider un email
     */
    public static function validateEmail($email) {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    /**
     * Valider un nom d'utilisateur
     */
    public static function validateUsername($username) {
        return preg_match('/^[a-zA-Z0-9_]{3,20}$/', $username);
    }
    
    /**
     * Valider un mot de passe
     */
    public static function validatePassword($password) {
        // Au moins 8 caractères, avec au moins une majuscule, une minuscule et un chiffre
        return strlen($password) >= 8 && 
               preg_match('/[A-Z]/', $password) && 
               preg_match('/[a-z]/', $password) && 
               preg_match('/[0-9]/', $password);
    }
    
    /**
     * Logger une action utilisateur
     */
    public static function logAction($user_id, $action, $details = null) {
        global $db;
        
        try {
            $db->query(
                "INSERT INTO user_actions (id, user_id, action, details, created_at) 
                 VALUES (?, ?, ?, ?, NOW())",
                [self::generateUUID(), $user_id, $action, json_encode($details)]
            );
        } catch (Exception $e) {
            error_log("Erreur lors du logging: " . $e->getMessage());
        }
    }
    
    /**
     * Créer un utilisateur admin par défaut
     */
    public static function createDefaultAdmin() {
        global $db;
        
        // Vérifier si un admin existe déjà
        $existingAdmin = $db->fetch("SELECT id FROM users WHERE role = 'admin' LIMIT 1");
        if ($existingAdmin) {
            return false; // Admin déjà existant
        }
        
        $adminId = self::generateUUID();
        $profileId = self::generateUUID();
        
        try {
            $db->beginTransaction();
            
            // Créer l'utilisateur admin
            $db->query(
                "INSERT INTO users (id, username, email, hashed_password, role, status, is_verified, created_at) 
                 VALUES (?, ?, ?, ?, 'admin', 'active', 1, NOW())",
                [
                    $adminId,
                    'admin',
                    'admin@oupafamilly.com',
                    self::hashPassword('Oupafamilly2024!')
                ]
            );
            
            // Créer le profil admin
            $db->query(
                "INSERT INTO user_profiles (id, user_id, display_name, bio, coins, created_at) 
                 VALUES (?, ?, ?, ?, ?, NOW())",
                [
                    $profileId,
                    $adminId,
                    'Administrateur Oupafamilly',
                    'Administrateur de la communauté Oupafamilly',
                    10000
                ]
            );
            
            $db->commit();
            return true;
            
        } catch (Exception $e) {
            $db->rollback();
            error_log("Erreur création admin: " . $e->getMessage());
            return false;
        }
    }
}

// Classe pour la gestion des réponses API
class ApiResponse {
    
    public static function success($data = null, $message = null) {
        http_response_code(200);
        $response = [];
        if ($message) $response['message'] = $message;
        if ($data !== null) $response = array_merge($response, is_array($data) ? $data : ['data' => $data]);
        echo json_encode($response);
    }
    
    public static function error($message, $code = 400, $details = null) {
        http_response_code($code);
        $response = ['error' => $message];
        if ($details) $response['details'] = $details;
        echo json_encode($response);
    }
    
    public static function notFound($message = 'Resource not found') {
        self::error($message, 404);
    }
    
    public static function unauthorized($message = 'Unauthorized') {
        self::error($message, 401);
    }
    
    public static function forbidden($message = 'Forbidden') {
        self::error($message, 403);
    }
    
    public static function serverError($message = 'Internal server error') {
        self::error($message, 500);
    }
}

// Classe pour les validations
class Validator {
    
    public static function required($value, $field) {
        if (empty($value)) {
            throw new Exception("$field is required");
        }
    }
    
    public static function email($email) {
        if (!Auth::validateEmail($email)) {
            throw new Exception("Invalid email format");
        }
    }
    
    public static function username($username) {
        if (!Auth::validateUsername($username)) {
            throw new Exception("Username must be 3-20 characters, alphanumeric and underscore only");
        }
    }
    
    public static function password($password) {
        if (!Auth::validatePassword($password)) {
            throw new Exception("Password must be at least 8 characters with uppercase, lowercase and number");
        }
    }
    
    public static function length($value, $min, $max, $field) {
        $len = strlen($value);
        if ($len < $min || $len > $max) {
            throw new Exception("$field must be between $min and $max characters");
        }
    }
    
    public static function inArray($value, $array, $field) {
        if (!in_array($value, $array)) {
            throw new Exception("$field must be one of: " . implode(', ', $array));
        }
    }
}
?>