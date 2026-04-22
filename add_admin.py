#!/usr/bin/env python3
"""
Add admin account to existing database
"""

from app import app, db, User

def add_admin_account():
    """Add admin account to existing database"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin account already exists!")
            print("Username: admin")
            print("Password: admin123")
            return
        
        # Create admin account
        admin = User(
            username='admin',
            email='admin@focus.org',
            full_name='Tokuma Adamu',
            user_type='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Full Name: Tokuma Adamu")

if __name__ == '__main__':
    add_admin_account()
