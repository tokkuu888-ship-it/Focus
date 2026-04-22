#!/usr/bin/env python3
"""
Check if admin account exists in database
"""

from app import app, db, User

def check_admin_account():
    """Check if admin account exists"""
    with app.app_context():
        # Check for admin account
        admin_user = User.query.filter_by(username='admin').first()
        
        print("=== ADMIN ACCOUNT CHECK ===")
        if admin_user:
            print(f"✅ Admin account found:")
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Full Name: {admin_user.full_name}")
            print(f"   User Type: {admin_user.user_type}")
            print(f"   ID: {admin_user.id}")
            
            # Test password verification
            if admin_user.check_password('admin123'):
                print(f"   ✅ Password verification: SUCCESS")
            else:
                print(f"   ❌ Password verification: FAILED")
        else:
            print("❌ No admin account found!")
            
        print("\n=== ALL USERS IN DATABASE ===")
        all_users = User.query.all()
        for user in all_users:
            print(f"   {user.username} ({user.user_type}) - {user.full_name}")
        
        print("\n=== USER COUNTS ===")
        admin_count = User.query.filter_by(user_type='admin').count()
        counselor_count = User.query.filter_by(user_type='counselor').count()
        student_count = User.query.filter_by(user_type='student').count()
        
        print(f"   Admins: {admin_count}")
        print(f"   Counselors: {counselor_count}")
        print(f"   Students: {student_count}")
        print(f"   Total: {len(all_users)}")

if __name__ == '__main__':
    check_admin_account()
