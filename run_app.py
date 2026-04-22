#!/usr/bin/env python3
"""
Simple Flask app runner without auto-reload to avoid dependency issues
"""

from app import app, db, User

def create_sample_data():
    """Create sample users for testing"""
    with app.app_context():
        # Check if users already exist
        if User.query.first():
            print("Sample data already exists.")
            return
        
        # Create sample admin
        admin = User(
            username='admin',
            email='admin@focus.org',
            full_name='System Administrator',
            user_type='admin'
        )
        admin.set_password('admin123')
        
        # Create sample counselor
        counselor = User(
            username='counselor1',
            email='counselor@focus.org',
            full_name='Dr. Sarah Johnson',
            user_type='counselor'
        )
        counselor.set_password('counselor123')
        
        # Create sample student
        student = User(
            username='student1',
            email='student@focus.org',
            full_name='Tokuma Adamu',
            user_type='student'
        )
        student.set_password('student123')
        
        db.session.add(admin)
        db.session.add(counselor)
        db.session.add(student)
        db.session.commit()
        
        print("Sample users created:")
        print("Admin: username=admin, password=admin123")
        print("Counselor: username=counselor1, password=counselor123")
        print("Student: username=student1, password=student123")

if __name__ == '__main__':
    print("Starting FOCUS Counseling Platform...")
    print("Creating database tables...")
    
    with app.app_context():
        db.create_all()
    
    print("Creating sample data...")
    create_sample_data()
    
    print("=" * 50)
    print("PLATFORM READY!")
    print("Local Access: http://localhost:5000")
    print("=" * 50)
    print("\nTest Accounts:")
    print("Counselor: username=counselor1, password=counselor123")
    print("Student: username=student1, password=student123")
    print("\nStarting Flask app...")
    
    # Run without debug/auto-reload to avoid dependency issues
    app.run(host='0.0.0.0', port=5000, debug=False)
