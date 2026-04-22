#!/usr/bin/env python3
"""
Test the registration form to see all user type options
"""

from app import app, RegistrationForm

def test_registration_form():
    """Test registration form user type options"""
    with app.app_context():
        form = RegistrationForm()
        
        print("=== REGISTRATION FORM TEST ===")
        print("User Type Field:")
        print(f"  Label: {form.user_type.label}")
        print(f"  Choices: {form.user_type.choices}")
        
        print("\n=== AVAILABLE OPTIONS ===")
        for value, label in form.user_type.choices:
            print(f"  Value: '{value}' -> Label: '{label}'")
        
        print("\n=== EXPECTED VS ACTUAL ===")
        expected = [('student', 'Student'), ('counselor', 'Counselor'), ('admin', 'Administrator')]
        actual = form.user_type.choices
        
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        
        if expected == actual:
            print("  MATCH: All options are present!")
        else:
            print("  MISMATCH: Options are missing!")
            
            # Show what's missing
            expected_set = set(expected)
            actual_set = set(actual)
            missing = expected_set - actual_set
            if missing:
                print(f"  Missing: {missing}")

if __name__ == '__main__':
    test_registration_form()
