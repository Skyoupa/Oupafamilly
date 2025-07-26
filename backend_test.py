#!/usr/bin/env python3
"""
Backend API Testing for Oupafamilly Application
Tests all API endpoints using the public URL
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class OupafamillyAPITester:
    def __init__(self, base_url="https://bb92492e-ed19-4f17-8a23-4bc20c416fbd.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.admin_user_id = None

    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int, 
                 data: Optional[Dict] = None, headers: Optional[Dict] = None) -> tuple[bool, Dict]:
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if not endpoint.startswith('http') else endpoint
        
        # Default headers
        test_headers = {'Content-Type': 'application/json'}
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        self.log(f"Testing {name}...")
        self.log(f"  URL: {url}")
        self.log(f"  Method: {method}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.log(f"✅ PASSED - Status: {response.status_code}", "SUCCESS")
            else:
                self.log(f"❌ FAILED - Expected {expected_status}, got {response.status_code}", "ERROR")
                self.log(f"  Response: {response.text[:200]}...", "ERROR")

            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}

            return success, response_data

        except requests.exceptions.RequestException as e:
            self.log(f"❌ FAILED - Network Error: {str(e)}", "ERROR")
            return False, {}
        except Exception as e:
            self.log(f"❌ FAILED - Error: {str(e)}", "ERROR")
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        self.log("=== TESTING HEALTH CHECK ===")
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        if success:
            self.log(f"  Database status: {response.get('database', 'unknown')}")
        return success

    def test_root_endpoint(self):
        """Test root API endpoint"""
        self.log("=== TESTING ROOT ENDPOINT ===")
        success, response = self.run_test(
            "Root API",
            "GET",
            "",
            200
        )
        if success:
            self.log(f"  API Version: {response.get('version', 'unknown')}")
            self.log(f"  Available endpoints: {len(response.get('endpoints', {}))}")
        return success

    def test_admin_login(self):
        """Test admin login"""
        self.log("=== TESTING ADMIN LOGIN ===")
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data={
                "email": "admin@oupafamilly.com",
                "password": "Oupafamilly2024!"
            }
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.log(f"  Token obtained: {self.token[:20]}...", "SUCCESS")
            return True
        else:
            self.log("  Failed to get access token", "ERROR")
            return False

    def test_get_current_user(self):
        """Test getting current user info"""
        if not self.token:
            self.log("Skipping user info test - no token", "WARNING")
            return False
            
        self.log("=== TESTING GET CURRENT USER ===")
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        
        if success:
            self.admin_user_id = response.get('id')
            self.log(f"  User ID: {self.admin_user_id}")
            self.log(f"  Username: {response.get('username')}")
            self.log(f"  Role: {response.get('role')}")
        
        return success

    def test_admin_dashboard(self):
        """Test admin dashboard"""
        if not self.token:
            self.log("Skipping admin dashboard test - no token", "WARNING")
            return False
            
        self.log("=== TESTING ADMIN DASHBOARD ===")
        success, response = self.run_test(
            "Admin Dashboard",
            "GET",
            "admin/dashboard",
            200
        )
        
        if success:
            community = response.get('community_overview', {})
            self.log(f"  Total members: {community.get('total_members', 0)}")
            self.log(f"  Active members: {community.get('active_members', 0)}")
            tournaments = response.get('tournaments', {})
            self.log(f"  Total tournaments: {tournaments.get('total', 0)}")
        
        return success

    def test_tournaments_list(self):
        """Test getting tournaments list"""
        self.log("=== TESTING TOURNAMENTS LIST ===")
        success, response = self.run_test(
            "Get Tournaments",
            "GET",
            "tournaments/",
            200
        )
        
        if success:
            tournaments = response if isinstance(response, list) else []
            self.log(f"  Found {len(tournaments)} tournaments")
            if tournaments:
                self.log(f"  First tournament: {tournaments[0].get('title', 'No title')}")
        
        return success

    def test_tournament_stats(self):
        """Test tournament statistics"""
        self.log("=== TESTING TOURNAMENT STATS ===")
        success, response = self.run_test(
            "Tournament Stats",
            "GET",
            "tournaments/stats/community",
            200
        )
        
        if success:
            self.log(f"  Total tournaments: {response.get('total_tournaments', 0)}")
            self.log(f"  Active tournaments: {response.get('active_tournaments', 0)}")
            self.log(f"  Upcoming tournaments: {response.get('upcoming_tournaments', 0)}")
        
        return success

    def test_tournament_templates(self):
        """Test tournament templates"""
        self.log("=== TESTING TOURNAMENT TEMPLATES ===")
        success, response = self.run_test(
            "Tournament Templates",
            "GET",
            "tournaments/templates/popular",
            200
        )
        
        if success:
            templates = response.get('templates', [])
            self.log(f"  Found {len(templates)} templates")
            if templates:
                self.log(f"  First template: {templates[0].get('name', 'No name')}")
        
        return success

    def test_user_registration(self):
        """Test user registration"""
        self.log("=== TESTING USER REGISTRATION ===")
        test_user_data = {
            "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%H%M%S')}@test.com",
            "password": "TestPassword123!",
            "display_name": "Test User"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_user_data
        )
        
        if success:
            self.log(f"  New user ID: {response.get('id')}")
            self.log(f"  Username: {response.get('username')}")
            self.log(f"  Status: {response.get('status')}")
        
        return success

    def test_auth_stats(self):
        """Test authentication statistics (admin only)"""
        if not self.token:
            self.log("Skipping auth stats test - no token", "WARNING")
            return False
            
        self.log("=== TESTING AUTH STATS ===")
        success, response = self.run_test(
            "Auth Stats",
            "GET",
            "auth/stats",
            200
        )
        
        if success:
            self.log(f"  Total users: {response.get('total_users', 0)}")
            self.log(f"  Active users: {response.get('active_users', 0)}")
            self.log(f"  Recent registrations: {response.get('recent_registrations', 0)}")
        
        return success

    def test_status_endpoints(self):
        """Test status check endpoints"""
        self.log("=== TESTING STATUS ENDPOINTS ===")
        
        # Test creating status check
        success1, response1 = self.run_test(
            "Create Status Check",
            "POST",
            "status",
            200,
            data={"client_name": "test_client"}
        )
        
        # Test getting status checks
        success2, response2 = self.run_test(
            "Get Status Checks",
            "GET",
            "status",
            200
        )
        
        if success2:
            status_checks = response2 if isinstance(response2, list) else []
            self.log(f"  Found {len(status_checks)} status checks")
        
        return success1 and success2

    def test_cs2_economy_tutorial_french_translation(self):
        """Test specific CS2 Economy tutorial French translation - MAIN FOCUS"""
        self.log("=== TESTING CS2 ECONOMY TUTORIAL FRENCH TRANSLATION ===")
        
        # Get CS2 tutorials specifically
        success, response = self.run_test(
            "Get CS2 Tutorials for Economy Check",
            "GET",
            "content/tutorials?game=cs2",
            200
        )
        
        if not success:
            self.log("❌ Failed to get CS2 tutorials", "ERROR")
            return False
        
        tutorials = response if isinstance(response, list) else []
        economy_tutorial = None
        
        # Find the specific economy tutorial
        for tutorial in tutorials:
            if "Économie CS2" in tutorial.get('title', '') and "comprendre les achats" in tutorial.get('title', ''):
                economy_tutorial = tutorial
                break
        
        if not economy_tutorial:
            self.log("❌ Economy tutorial 'Économie CS2 : comprendre les achats' not found", "ERROR")
            return False
        
        self.log(f"✅ Found Economy Tutorial: {economy_tutorial.get('title')}")
        
        # Get full tutorial details
        tutorial_id = economy_tutorial.get('id')
        success_detail, tutorial_detail = self.run_test(
            "Get Economy Tutorial Details",
            "GET",
            f"content/tutorials/{tutorial_id}",
            200
        )
        
        if not success_detail:
            self.log("❌ Failed to get economy tutorial details", "ERROR")
            return False
        
        content = tutorial_detail.get('content', '')
        title = tutorial_detail.get('title', '')
        
        self.log(f"  Tutorial Title: {title}")
        self.log(f"  Content Length: {len(content)} characters")
        
        # Check for specific French translations that were mentioned in the context
        translation_checks = [
            ("Élite", "Elite → Élite translation"),
            ("Niveau 1", "Tier 1 → Niveau 1 translation"),
            ("SITUATIONS DE FORCE-BUY", "FORCE-BUY SITUATIONS → SITUATIONS DE FORCE-BUY translation"),
            ("Validé professionnellement", "Professional validated → Validé professionnellement translation")
        ]
        
        translation_success = True
        for french_term, description in translation_checks:
            if french_term in content:
                self.log(f"  ✅ {description}: Found '{french_term}'")
            else:
                self.log(f"  ❌ {description}: Missing '{french_term}'", "ERROR")
                translation_success = False
        
        # Check for remaining English terms that should have been translated
        english_terms_to_avoid = [
            "Elite",
            "Tier 1", 
            "FORCE-BUY SITUATIONS (Professional validated)",
            "Professional validated"
        ]
        
        english_found = []
        for english_term in english_terms_to_avoid:
            if english_term in content:
                english_found.append(english_term)
        
        if english_found:
            self.log(f"  ❌ Found untranslated English terms: {english_found}", "ERROR")
            translation_success = False
        else:
            self.log("  ✅ No problematic English terms found")
        
        # Check overall French content quality
        french_indicators = ["les", "des", "une", "dans", "pour", "avec", "sur", "par", "de", "du", "la", "le"]
        french_count = sum(content.lower().count(indicator) for indicator in french_indicators)
        
        if french_count > 10:  # Should have plenty of French words
            self.log(f"  ✅ Content appears to be in French (French indicators: {french_count})")
        else:
            self.log(f"  ❌ Content may not be fully in French (French indicators: {french_count})", "ERROR")
            translation_success = False
        
        # Show a sample of the content for verification
        content_sample = content[:300] + "..." if len(content) > 300 else content
        self.log(f"  Content Sample: {content_sample}")
        
        return translation_success

    def test_tutorials_endpoints(self):
        """Test tutorial endpoints - MAIN FOCUS FOR VALIDATION"""
        self.log("=== TESTING TUTORIALS ENDPOINTS ===")
        
        # Test getting all tutorials with limit 100 (key requirement)
        success1, response1 = self.run_test(
            "Get All Tutorials (Limit 100)",
            "GET",
            "content/tutorials?limit=100",
            200
        )
        
        total_tutorials = 0
        games_count = {}
        
        if success1:
            tutorials = response1 if isinstance(response1, list) else []
            total_tutorials = len(tutorials)
            self.log(f"  Found {total_tutorials} tutorials total")
            
            # Count tutorials per game
            games_found = set()
            levels_found = set()
            for tutorial in tutorials:
                if 'game' in tutorial:
                    game = tutorial['game']
                    games_found.add(game)
                    games_count[game] = games_count.get(game, 0) + 1
                if 'level' in tutorial:
                    levels_found.add(tutorial['level'])
            
            self.log(f"  Games found: {sorted(games_found)}")
            self.log(f"  Levels found: {sorted(levels_found)}")
            self.log(f"  Tutorials per game: {games_count}")
            
            # Validate expected 12 tutorials per game
            expected_games = ['cs2', 'wow', 'lol', 'sc2', 'minecraft']
            for game in expected_games:
                count = games_count.get(game, 0)
                if count == 12:
                    self.log(f"  ✅ {game.upper()}: {count} tutorials (CORRECT)")
                else:
                    self.log(f"  ❌ {game.upper()}: {count} tutorials (EXPECTED 12)", "ERROR")
            
            # Validate total is 60 (12 × 5 games)
            if total_tutorials == 60:
                self.log(f"  ✅ Total tutorials: {total_tutorials} (CORRECT)")
            else:
                self.log(f"  ❌ Total tutorials: {total_tutorials} (EXPECTED 60)", "ERROR")
        
        # Test each game individually using by-game endpoint
        expected_games = ['cs2', 'wow', 'lol', 'sc2', 'minecraft']
        game_tests_success = True
        
        for game in expected_games:
            success_game, response_game = self.run_test(
                f"Get {game.upper()} Tutorials by Game",
                "GET",
                f"content/tutorials/by-game/{game}",
                200
            )
            
            if success_game:
                total_for_game = response_game.get('total_tutorials', 0)
                tutorials_by_level = response_game.get('tutorials_by_level', {})
                
                if total_for_game == 12:
                    self.log(f"  ✅ {game.upper()} by-game endpoint: {total_for_game} tutorials (CORRECT)")
                else:
                    self.log(f"  ❌ {game.upper()} by-game endpoint: {total_for_game} tutorials (EXPECTED 12)", "ERROR")
                    game_tests_success = False
                
                # Show level distribution
                for level, tuts in tutorials_by_level.items():
                    self.log(f"    {level}: {len(tuts)} tutorials")
            else:
                game_tests_success = False
        
        # Test tutorial detail endpoint with first tutorial if available
        success_detail = True
        if success1 and response1:
            tutorials = response1 if isinstance(response1, list) else []
            if tutorials:
                first_tutorial = tutorials[0]
                tutorial_id = first_tutorial.get('id')
                if tutorial_id:
                    success_detail, response_detail = self.run_test(
                        f"Get Tutorial Detail",
                        "GET",
                        f"content/tutorials/{tutorial_id}",
                        200
                    )
                    if success_detail:
                        self.log(f"  Tutorial detail: {response_detail.get('title', 'No title')}")
                        self.log(f"  Game: {response_detail.get('game', 'No game')}")
                        self.log(f"  Level: {response_detail.get('level', 'No level')}")
                        self.log(f"  Content length: {len(response_detail.get('content', ''))}")
                        self.log(f"  Has image: {'image' in response_detail and response_detail['image']}")
        
        # Test filtering capabilities
        success_filter, response_filter = self.run_test(
            "Get Beginner Tutorials",
            "GET",
            "content/tutorials?level=beginner",
            200
        )
        
        if success_filter:
            beginner_tutorials = response_filter if isinstance(response_filter, list) else []
            self.log(f"  Beginner tutorials found: {len(beginner_tutorials)}")
        
        return success1 and game_tests_success and success_detail and success_filter

    def test_content_stats(self):
        """Test content statistics endpoint"""
        if not self.token:
            self.log("Skipping content stats test - no token", "WARNING")
            return False
            
        self.log("=== TESTING CONTENT STATS ===")
        success, response = self.run_test(
            "Content Statistics",
            "GET",
            "content/stats/content",
            200
        )
        
        if success:
            tutorials = response.get('tutorials', {})
            self.log(f"  Total tutorials: {tutorials.get('total', 0)}")
            self.log(f"  Recent tutorials: {tutorials.get('recent', 0)}")
            
            by_game = tutorials.get('by_game', [])
            self.log(f"  Tutorials by game: {len(by_game)} games")
            for game_stat in by_game:
                self.log(f"    {game_stat.get('game')}: {game_stat.get('count')} tutorials")
        
        return success

    def run_all_tests(self):
        """Run all API tests"""
        self.log("🚀 Starting Oupafamilly API Tests")
        self.log(f"Base URL: {self.base_url}")
        self.log(f"API URL: {self.api_url}")
        
        # Basic connectivity tests
        self.test_health_check()
        self.test_root_endpoint()
        
        # Authentication tests
        if self.test_admin_login():
            self.test_get_current_user()
            self.test_admin_dashboard()
            self.test_auth_stats()
            self.test_content_stats()
        
        # Public endpoints
        self.test_tournaments_list()
        self.test_tournament_stats()
        self.test_tournament_templates()
        self.test_status_endpoints()
        
        # MAIN FOCUS: Tutorial endpoints testing
        self.test_tutorials_endpoints()
        
        # User registration (should work without auth)
        self.test_user_registration()
        
        # Print final results
        self.log("=" * 50)
        self.log(f"📊 FINAL RESULTS:")
        self.log(f"Tests Run: {self.tests_run}")
        self.log(f"Tests Passed: {self.tests_passed}")
        self.log(f"Tests Failed: {self.tests_run - self.tests_passed}")
        self.log(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            self.log("🎉 ALL TESTS PASSED!", "SUCCESS")
            return 0
        else:
            self.log("❌ SOME TESTS FAILED!", "ERROR")
            return 1

def main():
    """Main test runner"""
    tester = OupafamillyAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())