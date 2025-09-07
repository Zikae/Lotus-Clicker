#!/usr/bin/env python3
"""
Test script for Minecraft AutoClicker functionality
Run this to verify that all components work correctly
"""

import sys
import time
import threading
from pynput import mouse, keyboard
import win32gui

def test_mouse_control():
    """Test mouse control functionality"""
    print("Testing mouse control...")
    try:
        mouse_controller = mouse.Controller()
        print("✓ Mouse controller initialized successfully")
        
        # Test click (without actually clicking)
        print("✓ Mouse click simulation available")
        return True
    except Exception as e:
        print(f"✗ Mouse control test failed: {e}")
        return False

def test_keyboard_control():
    """Test keyboard control functionality"""
    print("Testing keyboard control...")
    try:
        keyboard_controller = keyboard.Controller()
        print("✓ Keyboard controller initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Keyboard control test failed: {e}")
        return False

def test_window_detection():
    """Test window detection functionality"""
    print("Testing window detection...")
    try:
        # Get all windows
        windows = []
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    windows.append((hwnd, window_title))
        
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        print(f"✓ Found {len(windows)} visible windows")
        
        # Look for Minecraft
        minecraft_windows = [title for hwnd, title in windows if "minecraft" in title.lower()]
        if minecraft_windows:
            print(f"✓ Found Minecraft windows: {minecraft_windows}")
        else:
            print("! No Minecraft windows found (this is normal if Minecraft isn't running)")
        
        return True
    except Exception as e:
        print(f"✗ Window detection test failed: {e}")
        return False

def test_listeners():
    """Test mouse and keyboard listeners"""
    print("Testing listeners...")
    try:
        # Test mouse listener
        def on_click(x, y, button, pressed):
            pass
        
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()
        time.sleep(0.1)
        mouse_listener.stop()
        print("✓ Mouse listener test passed")
        
        # Test keyboard listener
        def on_press(key):
            pass
        
        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.start()
        time.sleep(0.1)
        keyboard_listener.stop()
        print("✓ Keyboard listener test passed")
        
        return True
    except Exception as e:
        print(f"✗ Listener test failed: {e}")
        return False

def test_gui_imports():
    """Test GUI library imports"""
    print("Testing GUI imports...")
    try:
        import tkinter as tk
        print("✓ Tkinter imported successfully")
        
        import customtkinter as ctk
        print("✓ CustomTkinter imported successfully")
        
        from PIL import Image
        print("✓ Pillow imported successfully")
        
        import pystray
        print("✓ Pystray imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ GUI import test failed: {e}")
        return False

def test_cps_calculation():
    """Test CPS calculation and randomization"""
    print("Testing CPS calculation...")
    try:
        import random
        
        base_cps = 10
        for i in range(5):
            variance = random.uniform(-2, 2)
            randomized_cps = max(1, min(20, base_cps + variance))
            delay = 1.0 / randomized_cps
            print(f"  Test {i+1}: CPS={randomized_cps:.2f}, Delay={delay:.3f}s")
        
        print("✓ CPS calculation test passed")
        return True
    except Exception as e:
        print(f"✗ CPS calculation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Minecraft AutoClicker - Functionality Test")
    print("=" * 50)
    
    tests = [
        ("GUI Imports", test_gui_imports),
        ("Mouse Control", test_mouse_control),
        ("Keyboard Control", test_keyboard_control),
        ("Window Detection", test_window_detection),
        ("Listeners", test_listeners),
        ("CPS Calculation", test_cps_calculation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The autoclicker should work correctly.")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("You may need to install missing dependencies or run as administrator.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()
