#!/usr/bin/env python3
"""
Update student account name to Tokuma Adamu
"""

from app import app, db, User

def update_student_name():
    """Update student account name"""
    with app.app_context():
        # Find the student account
        student = User.query.filter_by(username='student1').first()
        if student:
            student.full_name = 'Tokuma Adamu'
            db.session.commit()
            print("Student name updated to: Tokuma Adamu")
        else:
            print("Student account not found")

if __name__ == '__main__':
    update_student_name()
