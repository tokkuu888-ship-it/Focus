#!/usr/bin/env python3
"""
Start ngrok with direct URL and no warnings
"""

import subprocess
import time
import requests

def start_ngrok_direct():
    """Start ngrok with direct access"""
    try:
        print("Starting ngrok with direct access...")
        
        # Kill any existing ngrok processes
        subprocess.run(["taskkill", "/F", "/IM", "ngrok.exe"], capture_output=True)
        time.sleep(1)
        
        # Start ngrok with all skip options
        process = subprocess.Popen([
            "ngrok", "http", "5000",
            "--ngrok-skip-browser-warning",
            "--log=stdout"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for ngrok to start
        time.sleep(4)
        
        # Get the public URL
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            tunnels = response.json()
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"\n✅ NGROK URL READY!")
                print(f"🌐 Public URL: {public_url}")
                print(f"📱 Mobile Access: {public_url}")
                print(f"💻 Desktop Access: {public_url}")
                print(f"\n🚀 Share this URL - NO WARNING PAGE!")
                print(f"✨ Direct access to FOCUS Counseling Platform")
                return process, public_url
        except Exception as e:
            print(f"Error getting ngrok URL: {e}")
            return process, None
            
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None, None

def main():
    print("="*70)
    print("🚀 FOCUS COUNSELING PLATFORM - NGROK DIRECT ACCESS")
    print("="*70)
    
    process, url = start_ngrok_direct()
    
    if process:
        print("\n" + "="*70)
        print("📋 PLATFORM INFORMATION")
        print("="*70)
        print(f"🏠 Local Access:     http://localhost:5000")
        print(f"🌐 Network Access:   http://10.6.196.178:5000")
        print(f"🔗 Public Access:    {url}")
        print("="*70)
        print("\n👥 TEST ACCOUNTS:")
        print("🔧 Admin:      username=admin,     password=admin123")
        print("👨‍⚕️ Counselor:  username=counselor1, password=counselor123")
        print("👨‍🎓 Student:    username=student1,   password=student123")
        print("="*70)
        print("\n✅ READY FOR USE!")
        print("📱 Share the Public URL with users")
        print("🔥 No browser warnings - direct access!")
        print("\nPress Ctrl+C to stop")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping ngrok...")
            process.terminate()

if __name__ == '__main__':
    main()
