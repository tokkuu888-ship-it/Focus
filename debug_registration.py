#!/usr/bin/env python3
"""
Debug the registration form to check user type options
"""

from flask import Flask
from app import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'

def debug_registration():
    """Debug registration form"""
    with app.app_context():
        form = RegistrationForm()
        
        print("=== REGISTRATION FORM DEBUG ===")
        print("User Type Field:")
        print(f"  Field Type: {type(form.user_type)}")
        print(f"  Label: {form.user_type.label}")
        print(f"  Choices: {form.user_type.choices}")
        
        print("\n=== CHOICES BREAKDOWN ===")
        for i, (value, label) in enumerate(form.user_type.choices):
            print(f"  {i+1}. Value: '{value}' -> Label: '{label}'")
        
        print("\n=== EXPECTED CHOICES ===")
        expected = [
            ('admin', 'Admin username/email'),
            ('counselor', 'Counselor'),
            ('student', 'Student')
        ]
        print(f"Expected: {expected}")
        
        print("\n=== COMPARISON ===")
        actual = form.user_type.choices
        if expected == actual:
            print("  MATCH: All choices present!")
        else:
            print("  MISMATCH: Missing choices!")
            expected_set = set(expected)
            actual_set = set(actual)
            missing = expected_set - actual_set
            extra = actual_set - expected_set
            if missing:
                print(f"  Missing: {missing}")
            if extra:
                print(f"  Extra: {extra}")

if __name__ == '__main__':
    debug_registration()
