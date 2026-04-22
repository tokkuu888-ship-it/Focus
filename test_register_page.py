#!/usr/bin/env python3
"""
Test the registration page to ensure user types are visible
"""

import requests
from bs4 import BeautifulSoup

def test_registration_page():
    """Test the registration page HTML"""
    try:
        # Get the registration page
        response = requests.get('http://localhost:5000/register')
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("=== REGISTRATION PAGE TEST ===")
            print(f"Page Status: {response.status_code}")
            
            # Find the user type select
            user_type_select = soup.find('select', {'name': 'user_type'})
            
            if user_type_select:
                print("User type select found!")
                
                # Get all options
                options = user_type_select.find_all('option')
                print(f"Number of options: {len(options)}")
                
                for i, option in enumerate(options):
                    value = option.get('value', '')
                    text = option.text.strip()
                    print(f"  {i+1}. Value: '{value}' -> Text: '{text}'")
                
                # Check for admin option
                admin_option = user_type_select.find('option', {'value': 'admin'})
                if admin_option:
                    print("  Admin option found: ", admin_option.text.strip())
                else:
                    print("  Admin option NOT found!")
            else:
                print("User type select NOT found!")
                
                # Look for any select elements
                selects = soup.find_all('select')
                print(f"Found {len(selects)} select elements:")
                for i, sel in enumerate(selects):
                    name = sel.get('name', 'no-name')
                    print(f"  {i+1}. Select name: '{name}'")
        else:
            print(f"Failed to load page: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_registration_page()
