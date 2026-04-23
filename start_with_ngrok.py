#!/usr/bin/env python3
"""
FOCUS Counseling Platform Startup Script with Ngrok
This script starts the Flask application and automatically creates an ngrok tunnel
for public access on both mobile and desktop devices.
"""

import os
import sys
import time
import threading
import requests
import subprocess
from flask import Flask
from app import app, db

def install_requirements():
    """Install required packages if not already installed"""
    print("Checking and installing required packages...")
    try:
        import flask
        import flask_sqlalchemy
        import flask_wtf
        import wtforms
        import werkzeug
        print("All required packages are already installed.")
    except ImportError as e:
        print(f"Missing package: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")

def setup_ngrok():
    """Setup and configure ngrok"""
    print("Setting up ngrok...")
    
    # Check if ngrok is installed
    try:
        subprocess.run(["ngrok", "version"], capture_output=True, check=True)
        print("ngrok is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ngrok not found. Please install ngrok first:")
        print("1. Download ngrok from https://ngrok.com/download")
        print("2. Extract and add to PATH, or place in this directory")
        print("3. Run: ngrok authtoken YOUR_AUTH_TOKEN")
        return None
    
    # Start ngrok tunnel
    try:
        print("Starting ngrok tunnel for port 5000...")
        ngrok_process = subprocess.Popen(
            ["ngrok", "http", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"ngrok tunnel established: {public_url}")
                print(f"Share this URL for mobile and desktop access!")
                return ngrok_process, public_url
        except:
            print("Could not retrieve ngrok URL from API")
            print("Check ngrok web interface at http://localhost:4040")
            return ngrok_process, None
            
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None, None

def create_sample_data():
    """Create sample users for testing"""
    print("Creating sample data...")
    with app.app_context():
        # Check if users already exist
        if User.query.first():
            print("Sample data already exists.")
            return
        
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
            full_name='Tokuma Adamu!',
            user_type='student'
        )
        student.set_password('student123')
        
        db.session.add(counselor)
        db.session.add(student)
        db.session.commit()
        
        print("Sample users created:")
        print("Counselor: username=counselor1, password=counselor123")
        print("Student: username=student1, password=student123")

def run_flask_app():
    """Run the Flask application"""
    print("Starting FOCUS Counseling Platform...")
    print("Flask app will be available at:")
    print("  - Local: http://localhost:5000")
    print("  - Network: http://0.0.0.0:5000")
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Create sample data
    create_sample_data()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

def main():
    """Main function to start the application with ngrok"""
    print("=" * 60)
    print("FOCUS Counseling Platform - Startup Script")
    print("=" * 60)
    
    # Install requirements
    install_requirements()
    
    # Setup ngrok
    ngrok_process, public_url = setup_ngrok()
    
    if ngrok_process:
        print("\n" + "=" * 60)
        print("PLATFORM READY FOR USE!")
        print("=" * 60)
        print(f"Local Access: http://localhost:5000")
        if public_url:
            print(f"Public Access: {public_url}")
            print(f"Mobile Access: {public_url}")
        print("=" * 60)
        print("\nTest Accounts:")
        print("Counselor Login:")
        print("  Username: counselor1")
        print("  Password: counselor123")
        print("\nStudent Login:")
        print("  Username: student1")
        print("  Password: student123")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60)
        
        try:
            # Start Flask app in the main thread
            run_flask_app()
        except KeyboardInterrupt:
            print("\nShutting down...")
            if ngrok_process:
                ngrok_process.terminate()
            print("Server stopped.")
    else:
        print("Failed to start ngrok. Starting Flask app only...")
        run_flask_app()

if __name__ == '__main__':
    main()
