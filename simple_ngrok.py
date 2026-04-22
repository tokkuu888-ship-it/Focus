#!/usr/bin/env python3
"""
Simple ngrok setup for FOCUS Counseling Platform
"""

import subprocess
import time
import requests

def start_ngrok_simple():
    """Start ngrok without any special flags"""
    try:
        print("Starting ngrok...")
        
        # Kill any existing ngrok processes
        subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], capture_output=True)
        time.sleep(2)
        
        # Start ngrok normally
        process = subprocess.Popen([
            "ngrok", "http", "5000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for ngrok to start
        time.sleep(5)
        
        # Get the public URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=10)
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                return process, public_url
        except Exception as e:
            print(f"Error getting ngrok URL: {e}")
            return process, None
            
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None, None

def main():
    print("="*60)
    print("🚀 FOCUS COUNSELING PLATFORM - SIMPLE NGROK")
    print("="*60)
    
    process, url = start_ngrok_simple()
    
    if process and url:
        print("\n" + "="*60)
        print("📋 PLATFORM ACCESS")
        print("="*60)
        print(f"🏠 Local:     http://localhost:5000")
        print(f"🌐 Network:   http://10.6.196.178:5000")
        print(f"🔗 Public:    {url}")
        print("="*60)
        print("\n👥 TEST ACCOUNTS:")
        print("🔧 Admin:      username=admin,     password=admin123")
        print("👨‍⚕️ Counselor:  username=counselor1, password=counselor123")
        print("👨‍🎓 Student:    username=student1,   password=student123")
        print("="*60)
        print("\n⚠️  NGROK WARNING INFO:")
        print("If you see ngrok warning page, click 'Visit Site' button")
        print("This is normal for free ngrok accounts")
        print("="*60)
        print("\n✅ PLATFORM READY!")
        print("Press Ctrl+C to stop")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping ngrok...")
            process.terminate()
    else:
        print("❌ Failed to start ngrok")

if __name__ == '__main__':
    main()
