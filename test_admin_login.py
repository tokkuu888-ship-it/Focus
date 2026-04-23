#!/usr/bin/env python3
"""
Test Admin login functionality
"""

from app import app, User

def test_admin_login():
    """Test admin login credentials"""
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("=== ADMIN LOGIN TEST ===")
            print(f"Username: {admin.username}")
            print(f"Full Name: {admin.full_name}")
            print(f"User Type: {admin.user_type}")
            print(f"Password Hash: {admin.password_hash[:20]}...")
            
            # Test password verification
            test_passwords = ['admin123', 'admin', 'password', '123456']
            print("\n=== PASSWORD TEST ===")
            for pwd in test_passwords:
                result = admin.check_password(pwd)
                print(f"Password '{pwd}': {'SUCCESS' if result else 'FAILED'}")
            
            # Check for any other admin users
            print("\n=== ALL ADMIN USERS ===")
            admins = User.query.filter_by(user_type='admin').all()
            for admin_user in admins:
                print(f"- {admin_user.username} ({admin_user.full_name})")
                
        else:
            print("Admin user NOT found!")

if __name__ == '__main__':
    test_admin_login()
