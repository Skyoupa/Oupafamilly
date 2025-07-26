"""
Advanced Input Validation and Sanitization
"""

import re
import bleach
from typing import Any, Dict, List, Optional, Union
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, validator
from datetime import datetime
import html
import urllib.parse
from monitoring import app_logger, log_security_event

class SecurityValidator:
    """Advanced security validation utilities"""
    
    # Dangerous patterns to detect
    DANGEROUS_PATTERNS = [
        r'<script.*?>.*?</script>',  # Script tags
        r'javascript:',  # JavaScript protocol
        r'on\w+\s*=',  # Event handlers
        r'expression\s*\(',  # CSS expressions
        r'@import',  # CSS imports
        r'eval\s*\(',  # JavaScript eval
        r'setTimeout\s*\(',  # Timeouts
        r'setInterval\s*\(',  # Intervals
    ]
    
    # SQL injection patterns
    SQL_PATTERNS = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
        r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
        r'(\s*(\'|\"|;|\*|%|--|\||&|\$))',
        r'(\b(SCRIPT|EXEC|SP_|XP_)\b)',
    ]
    
    # Allowed HTML tags for rich content
    ALLOWED_HTML_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote'
    ]
    
    ALLOWED_HTML_ATTRIBUTES = {
        '*': ['class'],
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'width', 'height']
    }
    
    @classmethod
    def sanitize_html(cls, content: str, allow_tags: bool = True) -> str:
        """Sanitize HTML content"""
        if not content:
            return ""
        
        if allow_tags:
            # Allow limited HTML tags
            return bleach.clean(
                content,
                tags=cls.ALLOWED_HTML_TAGS,
                attributes=cls.ALLOWED_HTML_ATTRIBUTES,
                strip=True
            )
        else:
            # Strip all HTML
            return bleach.clean(content, tags=[], strip=True)
    
    @classmethod
    def detect_xss(cls, content: str) -> bool:
        """Detect potential XSS attempts"""
        if not content:
            return False
        
        content_lower = content.lower()
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def detect_sql_injection(cls, content: str) -> bool:
        """Detect potential SQL injection attempts"""
        if not content:
            return False
        
        content_upper = content.upper()
        
        for pattern in cls.SQL_PATTERNS:
            if re.search(pattern, content_upper, re.IGNORECASE):
                return True
        
        return False
    
    @classmethod
    def validate_username(cls, username: str) -> Dict[str, Any]:
        """Validate username with security checks"""
        if not username:
            return {"valid": False, "error": "Username is required"}
        
        # Length check
        if len(username) < 3 or len(username) > 30:
            return {"valid": False, "error": "Username must be between 3 and 30 characters"}
        
        # Character check
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return {"valid": False, "error": "Username can only contain letters, numbers, underscore, and hyphen"}
        
        # Security checks
        if cls.detect_xss(username) or cls.detect_sql_injection(username):
            log_security_event("malicious_username_attempt", details={"username": username})
            return {"valid": False, "error": "Username contains invalid characters"}
        
        # Reserved words
        reserved = ['admin', 'root', 'system', 'api', 'null', 'undefined', 'bot']
        if username.lower() in reserved:
            return {"valid": False, "error": "Username is reserved"}
        
        return {"valid": True, "sanitized": username.strip()}
    
    @classmethod
    def validate_email_advanced(cls, email: str) -> Dict[str, Any]:
        """Advanced email validation"""
        if not email:
            return {"valid": False, "error": "Email is required"}
        
        try:
            # Basic validation
            valid = validate_email(email)
            normalized_email = valid.email
            
            # Security checks
            if cls.detect_xss(email) or cls.detect_sql_injection(email):
                log_security_event("malicious_email_attempt", details={"email": email})
                return {"valid": False, "error": "Email contains invalid characters"}
            
            # Disposable email check (basic)
            disposable_domains = [
                '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
                'mailinator.com', 'yopmail.com'
            ]
            
            domain = normalized_email.split('@')[1].lower()
            if domain in disposable_domains:
                return {"valid": False, "error": "Disposable emails are not allowed"}
            
            return {"valid": True, "sanitized": normalized_email}
            
        except EmailNotValidError as e:
            return {"valid": False, "error": str(e)}
    
    @classmethod
    def sanitize_text_input(cls, text: str, max_length: int = 1000, user_id: str = None) -> Dict[str, Any]:
        """Sanitize general text input"""
        if not text:
            return {"valid": True, "sanitized": ""}
        
        # Length check
        if len(text) > max_length:
            return {"valid": False, "error": f"Text exceeds maximum length of {max_length} characters"}
        
        # Security checks
        if cls.detect_xss(text):
            log_security_event("xss_attempt", user_id=user_id, details={"content_snippet": text[:100]})
            return {"valid": False, "error": "Content contains potentially dangerous elements"}
        
        if cls.detect_sql_injection(text):
            log_security_event("sql_injection_attempt", user_id=user_id, details={"content_snippet": text[:100]})
            return {"valid": False, "error": "Content contains invalid characters"}
        
        # HTML sanitization
        sanitized = cls.sanitize_html(text, allow_tags=True)
        
        # Additional cleaning
        sanitized = html.unescape(sanitized)  # Decode HTML entities
        sanitized = sanitized.strip()  # Remove whitespace
        
        return {"valid": True, "sanitized": sanitized}
    
    @classmethod
    def validate_url(cls, url: str) -> Dict[str, Any]:
        """Validate URL input"""
        if not url:
            return {"valid": True, "sanitized": ""}
        
        try:
            # Parse URL
            parsed = urllib.parse.urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return {"valid": False, "error": "Only HTTP and HTTPS URLs are allowed"}
            
            # Check for malicious patterns
            if cls.detect_xss(url):
                log_security_event("malicious_url_attempt", details={"url": url})
                return {"valid": False, "error": "URL contains invalid characters"}
            
            # Rebuild clean URL
            clean_url = urllib.parse.urlunparse(parsed)
            
            return {"valid": True, "sanitized": clean_url}
            
        except Exception as e:
            return {"valid": False, "error": "Invalid URL format"}
    
    @classmethod
    def validate_password(cls, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        if not password:
            return {"valid": False, "error": "Password is required"}
        
        # Length check
        if len(password) < 8:
            return {"valid": False, "error": "Password must be at least 8 characters long"}
        
        if len(password) > 128:
            return {"valid": False, "error": "Password is too long"}
        
        # Strength checks
        has_lower = re.search(r'[a-z]', password)
        has_upper = re.search(r'[A-Z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password)
        
        strength_score = sum([bool(has_lower), bool(has_upper), bool(has_digit), bool(has_special)])
        
        if strength_score < 3:
            return {
                "valid": False, 
                "error": "Password must contain at least 3 of: lowercase, uppercase, numbers, special characters"
            }
        
        # Common password check (basic)
        common_passwords = ['password', '12345678', 'qwerty', 'abc123', 'password123']
        if password.lower() in common_passwords:
            return {"valid": False, "error": "Password is too common"}
        
        return {"valid": True, "strength": strength_score}

# Enhanced Pydantic models with validation
class SecureTextInput(BaseModel):
    """Pydantic model for secure text input"""
    content: str
    max_length: int = 1000
    
    @validator('content')
    def validate_content(cls, v, values):
        if not v:
            return v
        
        max_length = values.get('max_length', 1000)
        result = SecurityValidator.sanitize_text_input(v, max_length)
        
        if not result['valid']:
            raise ValueError(result['error'])
        
        return result['sanitized']

class SecureEmailInput(BaseModel):
    """Pydantic model for secure email input"""
    email: str
    
    @validator('email')
    def validate_email(cls, v):
        if not v:
            return v
        
        result = SecurityValidator.validate_email_advanced(v)
        
        if not result['valid']:
            raise ValueError(result['error'])
        
        return result['sanitized']

class SecureUsernameInput(BaseModel):
    """Pydantic model for secure username input"""
    username: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v:
            return v
        
        result = SecurityValidator.validate_username(v)
        
        if not result['valid']:
            raise ValueError(result['error'])
        
        return result['sanitized']

# Security middleware for request validation
def validate_request_security(request_data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
    """Validate entire request for security issues"""
    
    issues = []
    sanitized_data = {}
    
    for key, value in request_data.items():
        if isinstance(value, str) and value:
            # Check for XSS
            if SecurityValidator.detect_xss(value):
                log_security_event("xss_in_request", user_id=user_id, details={
                    "field": key,
                    "content_snippet": value[:100]
                })
                issues.append(f"Field '{key}' contains potentially dangerous content")
                continue
            
            # Check for SQL injection
            if SecurityValidator.detect_sql_injection(value):
                log_security_event("sql_injection_in_request", user_id=user_id, details={
                    "field": key,
                    "content_snippet": value[:100]
                })
                issues.append(f"Field '{key}' contains invalid characters")
                continue
            
            # Basic sanitization
            sanitized_data[key] = SecurityValidator.sanitize_html(value, allow_tags=False)
        else:
            sanitized_data[key] = value
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "sanitized_data": sanitized_data
    }

# Export validation utilities
validator = SecurityValidator()