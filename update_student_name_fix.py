#!/usr/bin/env python3
"""
Update student name from John Doe to Tokuma Adamu!
"""

from app import app, User, db

def update_student_name():
    """Update student name in database"""
    with app.app_context():
        # Find the student user
        student = User.query.filter_by(username='student1').first()
        
        if student:
            print("=== UPDATING STUDENT NAME ===")
            print(f"Current name: {student.full_name}")
            student.full_name = 'Tokuma Adamu!'
            db.session.commit()
            print(f"Updated name: {student.full_name}")
            print("Student name updated successfully!")
        else:
            print("Student user not found!")

if __name__ == '__main__':
    update_student_name()
