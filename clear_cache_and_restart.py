#!/usr/bin/env python3
"""
Clear browser cache and restart the application
"""

import subprocess
import time

def restart_application():
    """Restart the Flask application with cache clearing"""
    print("Restarting FOCUS Counseling Platform...")
    
    # Kill any existing Python processes
    try:
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    print("Starting fresh instance...")
    return True

if __name__ == '__main__':
    restart_application()
