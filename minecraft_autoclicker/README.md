# Minecraft AutoClicker

A professional, feature-rich autoclicker specifically designed for Minecraft Java Edition with advanced customization options and safety features.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
Double-click `run_autoclicker.bat` to start the application

### Option 2: Manual Launch
1. Open Command Prompt or PowerShell in this folder
2. Run: `python launcher.py`

### Option 3: Direct Launch
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python minecraft_autoclicker.py`

## 🎮 How to Use

### Basic Usage:
1. **Launch the app** - You'll see a modern dark-themed window with 4 tabs
2. **Go to "Left Click" tab** and enable the autoclicker
3. **Adjust CPS** using the slider (1-20 clicks per second)
4. **Enable "Hold Mode"** for hold-to-click functionality
5. **Enable "Only when focused"** to only work when Minecraft is active

### Key Features:
- **Hold Mode**: Hold down left mouse button to activate clicking
- **Toggle Mode**: Use F6 hotkey to toggle on/off
- **Randomization**: Adds human-like variance to clicking
- **Block Hit**: Configurable chance for block-hit delays
- **Visual Feedback**: See when clicking is active

### Hotkeys:
- **F6** - Toggle left-click autoclicker
- **F7** - Toggle right-click autoclicker  
- **F8** - Show/hide window
- **Ctrl+Shift+End** - Emergency stop

### System Tray:
- Click the X button to minimize to system tray
- Right-click tray icon for options (Show/Hide/Quit)

## 🔧 Testing

Run the test script to verify everything works:
```bash
python test_functionality.py
```

## 📁 Files Included:
- `minecraft_autoclicker.py` - Main application
- `launcher.py` - Smart launcher with dependency checking
- `run_autoclicker.bat` - Windows batch file for easy launching
- `test_functionality.py` - Comprehensive testing script
- `requirements.txt` - Required Python packages
- `README.md` - This file

## ⚠️ Important Notes:
- This autoclicker is designed to work safely with Minecraft Java Edition
- Uses legitimate input simulation (no memory injection)
- Includes randomization to mimic human clicking patterns
- Emergency stop functionality for quick deactivation
- Self-destruct feature for complete cleanup

## 🛡️ Safety Features:
- **Emergency Stop**: Press Ctrl+Shift+End anywhere to immediately stop everything
- **Self-Destruct**: Complete cleanup with config file deletion (optional)
- **Focus Detection**: Only works when Minecraft window is active
- **Human-like Behavior**: Randomized clicking patterns

Enjoy your Minecraft autoclicker! 🎮
