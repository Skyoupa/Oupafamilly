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
    def __init__(self, base_url="https://917b40b9-35ed-47fa-b3d2-baa88d58a65b.preview.emergentagent.com"):
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
        
        # Public endpoints
        self.test_tournaments_list()
        self.test_tournament_stats()
        self.test_tournament_templates()
        self.test_status_endpoints()
        
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