#!/usr/bin/env python3
"""
AKWAFLOW Website Startup Script
"""

import os
import sys
from app import app, init_db, create_upload_folder

def setup_environment():
    """Setup the environment for the application"""
    print("Setting up AKWAFLOW website...")
    
    # Initialize database
    print("Initializing database...")
    init_db()
    
    # Create upload folder
    print("Creating upload folder...")
    create_upload_folder()
    
    print("Setup complete!")

def run_development():
    """Run the application in development mode"""
    setup_environment()
    print("Starting AKWAFLOW website in development mode...")
    print("Access the website at: http://localhost:5000")
    print("Admin panel at: http://localhost:5000/admin")
    print("Default admin credentials: admin / admin123")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

def run_production():
    """Run the application in production mode"""
    setup_environment()
    print("Starting AKWAFLOW website in production mode...")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    
    if mode == 'prod':
        run_production()
    else:
        run_development()