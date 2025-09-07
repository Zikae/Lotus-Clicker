#!/usr/bin/env python3
"""
Minecraft AutoClicker Launcher
Simple launcher script with error handling and dependency checking
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'pynput',
        'customtkinter', 
        'pywin32',
        'Pillow',
        'pystray'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    """Main launcher function"""
    print("Minecraft AutoClicker Launcher")
    print("=" * 40)
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("Warning: This application is designed for Windows.")
        print("Some features may not work on other operating systems.")
        input("Press Enter to continue anyway...")
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them automatically? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                print("Failed to install dependencies. Please install them manually:")
                print("pip install -r requirements.txt")
                input("Press Enter to exit...")
                return
        else:
            print("Please install the missing dependencies manually:")
            print("pip install -r requirements.txt")
            input("Press Enter to exit...")
            return
    
    # Check if main script exists
    if not os.path.exists("minecraft_autoclicker.py"):
        print("Error: minecraft_autoclicker.py not found!")
        print("Please ensure you're running this from the correct directory.")
        input("Press Enter to exit...")
        return
    
    # Launch the main application
    print("Starting Minecraft AutoClicker...")
    try:
        import minecraft_autoclicker
        app = minecraft_autoclicker.MinecraftAutoClicker()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
