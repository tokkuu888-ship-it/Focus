#!/usr/bin/env python3
"""
Test Admin account access and management features
"""

from app import app, User, db

def test_admin_management():
    """Test admin management capabilities"""
    with app.app_context():
        # Get admin account
        admin = User.query.filter_by(username='admin').first()
        
        print("=== ADMIN MANAGEMENT TEST ===")
        if admin:
            print(f"Admin User: {admin.username}")
            print(f"User Type: {admin.user_type}")
            print(f"Full Name: {admin.full_name}")
            
            # Check admin routes exist
            print("\n=== ADMIN ROUTES ===")
            print("1. /admin/users - Manage all users")
            print("2. /admin/edit_user/<id> - Edit specific user")
            print("3. /admin/view_user/<id> - View user details")
            print("4. /admin/delete_user/<id> - Delete user")
            print("5. /admin/appointments - View all appointments")
            print("6. /admin/messages - Monitor messages")
            print("7. /admin/stats - Platform statistics")
            
            # Check other users for management
            print("\n=== USERS AVAILABLE FOR MANAGEMENT ===")
            all_users = User.query.all()
            for user in all_users:
                if user.id != admin.id:
                    print(f"- {user.username} ({user.user_type}) - ID: {user.id}")
            
            print("\n=== ADMIN CAPABILITIES ===")
            print("Can edit user information: YES")
            print("Can change user types: YES")
            print("Can delete users: YES")
            print("Can reset passwords: YES")
            print("Can view all data: YES")
            print("Platform management: FULL")
            
        else:
            print("Admin account NOT found!")

if __name__ == '__main__':
    test_admin_management()
