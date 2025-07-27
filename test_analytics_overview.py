#!/usr/bin/env python3
"""
Specific test for Analytics Overview endpoint - User object fix validation
"""

import requests
import json
from datetime import datetime

class AnalyticsOverviewTester:
    def __init__(self):
        self.base_url = "https://9830d5e9-641f-4c50-9f9c-7b286b384a09.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.token = None

    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def login_admin(self):
        """Login as admin to get token"""
        self.log("=== ADMIN LOGIN ===")
        
        try:
            response = requests.post(
                f"{self.api_url}/auth/login",
                json={
                    "email": "admin@oupafamilly.com",
                    "password": "Oupafamilly2024!"
                },
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                self.log(f"✅ Admin login successful")
                self.log(f"Token: {self.token[:20]}...")
                return True
            else:
                self.log(f"❌ Admin login failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Login error: {str(e)}", "ERROR")
            return False

    def test_analytics_overview(self):
        """Test the specific Analytics Overview endpoint"""
        if not self.token:
            self.log("❌ No token available", "ERROR")
            return False
            
        self.log("=== TESTING ANALYTICS OVERVIEW ENDPOINT ===")
        self.log("Testing fix for 'User' object is not subscriptable error")
        
        try:
            response = requests.get(
                f"{self.api_url}/analytics/overview",
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                },
                timeout=15
            )
            
            self.log(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                self.log("✅ SUCCESS: Analytics Overview returns 200 OK")
                self.log("✅ 'User' object is not subscriptable error FIXED!")
                
                try:
                    data = response.json()
                    
                    # Check expected structure
                    expected_sections = ['overview', 'user_engagement', 'gaming_activity', 'economy', 'achievements', 'realtime', 'performance']
                    found_sections = []
                    missing_sections = []
                    
                    for section in expected_sections:
                        if section in data:
                            found_sections.append(section)
                            self.log(f"  ✅ Section '{section}' present")
                        else:
                            missing_sections.append(section)
                            self.log(f"  ❌ Section '{section}' missing", "ERROR")
                    
                    # Show some data from each section
                    if 'overview' in data:
                        overview = data['overview']
                        self.log(f"  Overview status: {overview.get('status', 'unknown')}")
                        self.log(f"  Generated at: {overview.get('generated_at', 'unknown')}")
                    
                    if 'user_engagement' in data and data['user_engagement']:
                        engagement = data['user_engagement']
                        self.log(f"  Total users: {engagement.get('total_users', 0)}")
                        self.log(f"  Active users (7d): {engagement.get('active_users_7d', 0)}")
                    
                    if 'gaming_activity' in data and data['gaming_activity']:
                        gaming = data['gaming_activity']
                        self.log(f"  Total tournaments: {gaming.get('total_tournaments', 0)}")
                        self.log(f"  Most popular game: {gaming.get('most_popular_game', 'unknown')}")
                    
                    if 'economy' in data and data['economy']:
                        economy = data['economy']
                        self.log(f"  Total coins circulation: {economy.get('total_coins_circulation', 0)}")
                    
                    if 'achievements' in data and data['achievements']:
                        achievements = data['achievements']
                        self.log(f"  Total badges awarded: {achievements.get('total_badges_awarded', 0)}")
                    
                    if 'realtime' in data and data['realtime']:
                        realtime = data['realtime']
                        self.log(f"  Users online: {realtime.get('users_online', 0)}")
                    
                    if 'performance' in data and data['performance']:
                        performance = data['performance']
                        self.log(f"  API health: {performance.get('api_health', 'unknown')}")
                    
                    # Final assessment
                    if len(found_sections) == len(expected_sections):
                        self.log("🎉 PERFECT: All expected sections present!")
                        self.log("🎉 Ultimate Dashboard Analytics Overview 100% operational!")
                        return True
                    elif len(found_sections) >= 5:
                        self.log(f"✅ GOOD: {len(found_sections)}/{len(expected_sections)} sections present")
                        self.log("✅ Analytics Overview mostly working")
                        return True
                    else:
                        self.log(f"⚠️ PARTIAL: Only {len(found_sections)}/{len(expected_sections)} sections present", "WARNING")
                        return False
                        
                except json.JSONDecodeError:
                    self.log("❌ Invalid JSON response", "ERROR")
                    self.log(f"Response text: {response.text[:500]}", "ERROR")
                    return False
                    
            elif response.status_code == 500:
                self.log("❌ FAILED: Still getting 500 error", "ERROR")
                self.log("❌ 'User' object fix may not be complete", "ERROR")
                try:
                    error_data = response.json()
                    self.log(f"Error detail: {error_data.get('detail', 'Unknown error')}", "ERROR")
                except:
                    self.log(f"Error response: {response.text[:200]}", "ERROR")
                return False
            else:
                self.log(f"❌ Unexpected status code: {response.status_code}", "ERROR")
                self.log(f"Response: {response.text[:200]}", "ERROR")
                return False
                
        except requests.exceptions.Timeout:
            self.log("❌ Request timeout", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Request error: {str(e)}", "ERROR")
            return False

    def run_test(self):
        """Run the complete test"""
        self.log("🔧 ANALYTICS OVERVIEW ENDPOINT TEST - USER OBJECT FIX VALIDATION")
        self.log("=" * 70)
        
        if not self.login_admin():
            self.log("❌ Cannot proceed without admin login", "ERROR")
            return False
        
        success = self.test_analytics_overview()
        
        self.log("=" * 70)
        if success:
            self.log("🎉 TEST RESULT: SUCCESS ✅")
            self.log("✅ Analytics Overview endpoint fix is working!")
            self.log("✅ No more 'User' object is not subscriptable error")
            self.log("✅ Ultimate Dashboard Analytics Overview ready for production")
        else:
            self.log("❌ TEST RESULT: FAILED ❌")
            self.log("❌ Analytics Overview endpoint still has issues")
            self.log("❌ Further investigation needed")
        
        return success

if __name__ == "__main__":
    tester = AnalyticsOverviewTester()
    success = tester.run_test()
    exit(0 if success else 1)