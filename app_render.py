#!/usr/bin/env python3
"""
FOCUS Counseling Platform - Render Deployment
Production-ready Flask application for Render hosting
"""

import os
import sys
import sqlalchemy as sa
from app import app, db, User
from flask_wtf.csrf import CSRFProtect

# Initialize CSRF protection
csrf = CSRFProtect(app)

def create_admin_user():
    """Create admin user if not exists"""
    try:
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@focus.org',
                    full_name='Tokuma Adamu',
                    user_type='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
            else:
                print("Admin user already exists!")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False
    return True

def create_sample_data():
    """Create sample counselor and student users"""
    try:
        with app.app_context():
            # Check if sample data already exists
            counselor = User.query.filter_by(username='counselor1').first()
            student = User.query.filter_by(username='student1').first()
            
            if not counselor:
                counselor = User(
                    username='counselor1',
                    email='counselor@focus.org',
                    full_name='Dr. Sarah Johnson',
                    user_type='counselor'
                )
                counselor.set_password('counselor123')
                db.session.add(counselor)
                print("Counselor user created!")
            
            if not student:
                student = User(
                    username='student1',
                    email='student@focus.org',
                    full_name='Tokuma Adamu!',
                    user_type='student'
                )
                student.set_password('student123')
                db.session.add(student)
                print("Student user created!")
            
            db.session.commit()
            print("Sample data created successfully!")
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return False
    return True

def initialize_database():
    """Initialize database and create tables"""
    try:
        with app.app_context():
            print("� Checking database connection...")
            # Add '#' to start of these lines to disable them:
            # db.session.execute(sa.text('DROP SCHEMA public CASCADE;')) 
            # db.session.execute(sa.text('CREATE SCHEMA public;'))
            # db.session.commit()
            
            # Keep this one active so it ensures tables exist without deleting them
            db.create_all() 
            print("✅ Database is ready!")
            return True
    except Exception as e:
        print(f"⚠️ Reset failed, attempting standard creation: {e}")
        db.session.rollback()
        try:
            # Fallback to standard creation
            db.create_all()
            print("✅ Database tables created with standard method!")
            return True
        except Exception as e2:
            print(f"❌ Standard creation also failed: {e2}")
            return False

if __name__ == '__main__':
    try:
        print("🚀 Starting FOCUS Counseling Platform...")
        
        # Check database connection
        print("📊 Checking database connection...")
        if not initialize_database():
            print("❌ Database initialization failed!")
            sys.exit(1)
        
        # Create admin user and sample data
        print("👥 Creating sample users...")
        if not create_admin_user():
            print("❌ Admin user creation failed!")
            sys.exit(1)
        
        if not create_sample_data():
            print("❌ Sample data creation failed!")
            sys.exit(1)
        
        print("✅ FOCUS Counseling Platform Ready for Production!")
        print("📊 Admin Dashboard: /admin")
        print("👥 Test Accounts:")
        print("   Admin: admin / admin123")
        print("   Counselor: counselor1 / counselor123")
        print("   Student: student1 / student123")
        
        # Run the application
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Starting server on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
