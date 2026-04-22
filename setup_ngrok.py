#!/usr/bin/env python3
"""
Setup ngrok for the FOCUS Counseling Platform
"""

import subprocess
import sys
import time
import requests

def check_ngrok():
    """Check if ngrok is available"""
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True, check=True)
        print("✓ ngrok is installed:", result.stdout.strip())
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ ngrok is not installed or not in PATH")
        return False

def install_ngrok():
    """Provide instructions for ngrok installation"""
    print("\n" + "="*60)
    print("NGROK SETUP INSTRUCTIONS")
    print("="*60)
    print("1. Download ngrok from: https://ngrok.com/download")
    print("2. Extract ngrok.exe to this directory")
    print("3. Authenticate with your authtoken:")
    print("   ngrok authtoken YOUR_AUTH_TOKEN")
    print("4. Run this script again")
    print("="*60)
    print("\nAlternative: Use the local network URL:")
    print("http://10.6.196.178:5000")
    print("(This works on devices connected to the same network)")

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        print("Starting ngrok tunnel...")
        process = subprocess.Popen(
            ["ngrok", "http", "5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"\n✓ ngrok tunnel created successfully!")
                print(f"Public URL: {public_url}")
                print(f"Mobile Access: {public_url}")
                print(f"\nShare this URL with users to access the platform")
                print(f"Both desktop and mobile devices can use this URL")
                return process, public_url
        except Exception as e:
            print(f"Could not get ngrok URL: {e}")
            return process, None
            
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None, None

def main():
    print("FOCUS Counseling Platform - ngrok Setup")
    print("="*50)
    
    if not check_ngrok():
        install_ngrok()
        return
    
    process, url = start_ngrok()
    
    if process:
        print("\n" + "="*60)
        print("PLATFORM ACCESS URLs")
        print("="*60)
        print(f"Local Access:     http://localhost:5000")
        print(f"Network Access:   http://10.6.196.178:5000")
        if url:
            print(f"Public Access:    {url}")
        print("="*60)
        print("\nTest Accounts:")
        print("Counselor: username=counselor1, password=counselor123")
        print("Student:   username=student1, password=student123")
        print("\nPress Ctrl+C to stop ngrok")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\nStopping ngrok...")
            process.terminate()

if __name__ == '__main__':
    main()
