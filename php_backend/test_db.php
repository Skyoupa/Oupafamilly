<?php
/**
 * Test de connexion à la base MySQL OVH
 */

require_once 'config.php';

try {
    $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    
    echo "✅ Connexion MySQL OVH réussie !\n";
    echo "Server: " . DB_HOST . "\n";
    echo "Database: " . DB_NAME . "\n";
    echo "User: " . DB_USER . "\n";
    
    // Test d'une requête simple
    $result = $pdo->query("SELECT VERSION() as version")->fetch();
    echo "MySQL Version: " . $result['version'] . "\n";
    
    // Tester la création d'une table simple
    $pdo->exec("CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50))");
    echo "✅ Test création table réussi\n";
    
    // Nettoyer
    $pdo->exec("DROP TABLE test_table");
    echo "✅ Test nettoyage réussi\n";
    
    echo "\n🎉 Tous les tests MySQL sont passés avec succès !\n";
    
} catch (PDOException $e) {
    echo "❌ Erreur de connexion MySQL: " . $e->getMessage() . "\n";
    echo "Code d'erreur: " . $e->getCode() . "\n";
    
    // Diagnostics supplémentaires
    echo "\nDiagnostics:\n";
    echo "- Host: " . DB_HOST . "\n";
    echo "- Database: " . DB_NAME . "\n";
    echo "- User: " . DB_USER . "\n";
    echo "- Password length: " . strlen(DB_PASS) . " chars\n";
    
    exit(1);
}
?>