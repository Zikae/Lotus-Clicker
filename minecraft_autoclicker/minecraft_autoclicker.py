import tkinter as tk
import customtkinter as ctk
import threading
import time
import random
import json
import os
import sys
import win32gui
import win32con
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MinecraftAutoClicker:
    def __init__(self):
        self.config_file = "autoclicker_config.json"
        self.running = True
        self.left_click_active = False
        self.right_click_active = False
        self.left_click_thread = None
        self.right_click_thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.tray_icon = None

        # Default configuration
        self.config = {
            "left_click": {
                "enabled": False,
                "cps": 10,
                "randomization": True,
                "hold_mode": True,
                "only_when_focused": True,
                "block_hit_chance": 0,
                "visual_feedback": True
            },
            "right_click": {
                "enabled": False,
                "cps": 8,
                "randomization": True,
                "lmb_lock": False,
                "only_when_focused": True
            },
            "general": {
                "hotkey_left": "f6",
                "hotkey_right": "f7",
                "hotkey_toggle": "f8",
                "start_minimized": False,
                "delete_config_on_exit": False
            }
        }

        self.load_config()
        self.setup_gui()
        self.setup_listeners()
        self.setup_system_tray()

    def setup_gui(self):
        """Create the main GUI interface"""
        self.root = ctk.CTk()
        self.root.title("Minecraft AutoClicker")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Create main tabview
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add tabs
        self.tabview.add("Left Click")
        self.tabview.add("Right Click")
        self.tabview.add("General")
        self.tabview.add("Status")

        self.setup_left_click_tab()
        self.setup_right_click_tab()
        self.setup_general_tab()
        self.setup_status_tab()

        # Status bar
        self.status_frame = ctk.CTkFrame(self.root)
        self.status_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Status: Inactive",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=10)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_left_click_tab(self):
        """Setup left click settings tab"""
        tab = self.tabview.tab("Left Click")

        # Enable toggle
        self.left_enable_var = ctk.BooleanVar(value=self.config["left_click"]["enabled"])
        self.left_enable_switch = ctk.CTkSwitch(
            tab,
            text="Enable Left Click AutoClicker",
            variable=self.left_enable_var,
            command=self.toggle_left_click
        )
        self.left_enable_switch.pack(pady=10, padx=20, anchor="w")

        # CPS slider
        ctk.CTkLabel(tab, text="Clicks Per Second:").pack(pady=(20, 5), padx=20, anchor="w")
        self.left_cps_var = ctk.IntVar(value=self.config["left_click"]["cps"])
        self.left_cps_slider = ctk.CTkSlider(
            tab,
            from_=1,
            to=20,
            variable=self.left_cps_var,
            command=self.update_left_cps
        )
        self.left_cps_slider.pack(pady=5, padx=20, fill="x")

        self.left_cps_label = ctk.CTkLabel(tab, text=f"CPS: {self.left_cps_var.get()}")
        self.left_cps_label.pack(pady=5, padx=20, anchor="w")

        # Randomization toggle
        self.left_random_var = ctk.BooleanVar(value=self.config["left_click"]["randomization"])
        self.left_random_switch = ctk.CTkSwitch(
            tab,
            text="Enable Randomization (±1-2 CPS)",
            variable=self.left_random_var
        )
        self.left_random_switch.pack(pady=10, padx=20, anchor="w")

        # Hold mode toggle
        self.left_hold_var = ctk.BooleanVar(value=self.config["left_click"]["hold_mode"])
        self.left_hold_switch = ctk.CTkSwitch(
            tab,
            text="Hold Mode (click while holding LMB)",
            variable=self.left_hold_var
        )
        self.left_hold_switch.pack(pady=10, padx=20, anchor="w")

        # Focus requirement
        self.left_focus_var = ctk.BooleanVar(value=self.config["left_click"]["only_when_focused"])
        self.left_focus_switch = ctk.CTkSwitch(
            tab,
            text="Only when Minecraft is focused",
            variable=self.left_focus_var
        )
        self.left_focus_switch.pack(pady=10, padx=20, anchor="w")

        # Block hit chance
        ctk.CTkLabel(tab, text="Block Hit Chance (%):").pack(pady=(20, 5), padx=20, anchor="w")
        self.left_block_var = ctk.IntVar(value=self.config["left_click"]["block_hit_chance"])
        self.left_block_slider = ctk.CTkSlider(
            tab,
            from_=0,
            to=100,
            variable=self.left_block_var
        )
        self.left_block_slider.pack(pady=5, padx=20, fill="x")

        self.left_block_label = ctk.CTkLabel(tab, text=f"Block Hit: {self.left_block_var.get()}%")
        self.left_block_label.pack(pady=5, padx=20, anchor="w")

        # Visual feedback
        self.left_visual_var = ctk.BooleanVar(value=self.config["left_click"]["visual_feedback"])
        self.left_visual_switch = ctk.CTkSwitch(
            tab,
            text="Visual Feedback",
            variable=self.left_visual_var
        )
        self.left_visual_switch.pack(pady=10, padx=20, anchor="w")

    def setup_right_click_tab(self):
        """Setup right click settings tab"""
        tab = self.tabview.tab("Right Click")

        # Enable toggle
        self.right_enable_var = ctk.BooleanVar(value=self.config["right_click"]["enabled"])
        self.right_enable_switch = ctk.CTkSwitch(
            tab,
            text="Enable Right Click AutoClicker",
            variable=self.right_enable_var,
            command=self.toggle_right_click
        )
        self.right_enable_switch.pack(pady=10, padx=20, anchor="w")

        # CPS slider
        ctk.CTkLabel(tab, text="Clicks Per Second:").pack(pady=(20, 5), padx=20, anchor="w")
        self.right_cps_var = ctk.IntVar(value=self.config["right_click"]["cps"])
        self.right_cps_slider = ctk.CTkSlider(
            tab,
            from_=1,
            to=20,
            variable=self.right_cps_var,
            command=self.update_right_cps
        )
        self.right_cps_slider.pack(pady=5, padx=20, fill="x")

        self.right_cps_label = ctk.CTkLabel(tab, text=f"CPS: {self.right_cps_var.get()}")
        self.right_cps_label.pack(pady=5, padx=20, anchor="w")

        # Randomization toggle
        self.right_random_var = ctk.BooleanVar(value=self.config["right_click"]["randomization"])
        self.right_random_switch = ctk.CTkSwitch(
            tab,
            text="Enable Randomization (±1-2 CPS)",
            variable=self.right_random_var
        )
        self.right_random_switch.pack(pady=10, padx=20, anchor="w")

        # LMB lock
        self.right_lmb_var = ctk.BooleanVar(value=self.config["right_click"]["lmb_lock"])
        self.right_lmb_switch = ctk.CTkSwitch(
            tab,
            text="LMB Lock (hold LMB to right-click)",
            variable=self.right_lmb_var
        )
        self.right_lmb_switch.pack(pady=10, padx=20, anchor="w")

        # Focus requirement
        self.right_focus_var = ctk.BooleanVar(value=self.config["right_click"]["only_when_focused"])
        self.right_focus_switch = ctk.CTkSwitch(
            tab,
            text="Only when Minecraft is focused",
            variable=self.right_focus_var
        )
        self.right_focus_switch.pack(pady=10, padx=20, anchor="w")

    def setup_general_tab(self):
        """Setup general settings tab"""
        tab = self.tabview.tab("General")

        # Hotkey settings
        ctk.CTkLabel(tab, text="Hotkey Configuration:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 20), padx=20, anchor="w")

        # Left click hotkey
        ctk.CTkLabel(tab, text="Left Click Toggle:").pack(pady=5, padx=20, anchor="w")
        self.left_hotkey_var = ctk.StringVar(value=self.config["general"]["hotkey_left"])
        self.left_hotkey_entry = ctk.CTkEntry(tab, textvariable=self.left_hotkey_var, width=100)
        self.left_hotkey_entry.pack(pady=5, padx=20, anchor="w")

        # Right click hotkey
        ctk.CTkLabel(tab, text="Right Click Toggle:").pack(pady=5, padx=20, anchor="w")
        self.right_hotkey_var = ctk.StringVar(value=self.config["general"]["hotkey_right"])
        self.right_hotkey_entry = ctk.CTkEntry(tab, textvariable=self.right_hotkey_var, width=100)
        self.right_hotkey_entry.pack(pady=5, padx=20, anchor="w")

        # Show/hide hotkey
        ctk.CTkLabel(tab, text="Show/Hide Window:").pack(pady=5, padx=20, anchor="w")
        self.toggle_hotkey_var = ctk.StringVar(value=self.config["general"]["hotkey_toggle"])
        self.toggle_hotkey_entry = ctk.CTkEntry(tab, textvariable=self.toggle_hotkey_var, width=100)
        self.toggle_hotkey_entry.pack(pady=5, padx=20, anchor="w")

        # Emergency stop
        ctk.CTkLabel(tab, text="Emergency Stop: Ctrl+Shift+End", font=ctk.CTkFont(weight="bold")).pack(pady=20, padx=20, anchor="w")

        # Start minimized
        self.start_minimized_var = ctk.BooleanVar(value=self.config["general"]["start_minimized"])
        self.start_minimized_switch = ctk.CTkSwitch(
            tab,
            text="Start Minimized to System Tray",
            variable=self.start_minimized_var
        )
        self.start_minimized_switch.pack(pady=10, padx=20, anchor="w")

        # Delete config on exit
        self.delete_config_var = ctk.BooleanVar(value=self.config["general"]["delete_config_on_exit"])
        self.delete_config_switch = ctk.CTkSwitch(
            tab,
            text="Delete Config on Exit",
            variable=self.delete_config_var
        )
        self.delete_config_switch.pack(pady=10, padx=20, anchor="w")

        # Save/Load buttons
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(pady=20, padx=20, fill="x")

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Configuration",
            command=self.save_config
        )
        self.save_button.pack(side="left", padx=10, pady=10)

        self.load_button = ctk.CTkButton(
            button_frame,
            text="Load Configuration",
            command=self.load_config
        )
        self.load_button.pack(side="left", padx=10, pady=10)

    def setup_status_tab(self):
        """Setup status display tab"""
        tab = self.tabview.tab("Status")

        # Status display
        self.status_display = ctk.CTkTextbox(tab, height=300)
        self.status_display.pack(pady=20, padx=20, fill="both", expand=True)

        # Control buttons
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(pady=10, padx=20, fill="x")

        self.emergency_stop_button = ctk.CTkButton(
            button_frame,
            text="EMERGENCY STOP",
            fg_color="red",
            hover_color="darkred",
            command=self.emergency_stop
        )
        self.emergency_stop_button.pack(side="left", padx=10, pady=10)

        self.clear_log_button = ctk.CTkButton(
            button_frame,
            text="Clear Log",
            command=self.clear_status_log
        )
        self.clear_log_button.pack(side="left", padx=10, pady=10)

        self.log_status("AutoClicker initialized successfully")

    def setup_listeners(self):
        """Setup mouse and keyboard listeners"""
        try:
            self.mouse_listener = MouseListener(
                on_click=self.on_mouse_click,
                on_scroll=self.on_mouse_scroll
            )
            self.mouse_listener.start()

            self.keyboard_listener = KeyboardListener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            self.keyboard_listener.start()

        except Exception as e:
            self.log_status(f"Error setting up listeners: {e}")

    def setup_system_tray(self):
        """Setup system tray icon"""
        try:
            # Create a simple icon (you can replace this with a proper icon file)
            image = Image.new('RGB', (64, 64), color='blue')

            menu = pystray.Menu(
                item('Show', self.show_window),
                item('Hide', self.hide_window),
                pystray.Menu.SEPARATOR,
                item('Quit', self.quit_application)
            )

            self.tray_icon = pystray.Icon("MinecraftAutoClicker", image, "Minecraft AutoClicker", menu)

            # Start tray icon in a separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()

        except Exception as e:
            self.log_status(f"Error setting up system tray: {e}")

    def is_minecraft_focused(self):
        """Check if Minecraft window is focused"""
        try:
            active_window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(active_window)
            return "minecraft" in window_title.lower() or "java" in window_title.lower()
        except:
            return False

    def get_randomized_cps(self, base_cps, randomization_enabled):
        """Get randomized CPS value"""
        if not randomization_enabled:
            return base_cps

        # Add ±1-2 CPS variance
        variance = random.uniform(-2, 2)
        randomized_cps = max(1, min(20, base_cps + variance))
        return randomized_cps

    def left_click_loop(self):
        """Left click autoclicker loop"""
        while self.running and self.left_click_active:
            try:
                # Check focus requirement
                if self.left_focus_var.get() and not self.is_minecraft_focused():
                    time.sleep(0.1)
                    continue

                # Get randomized CPS
                base_cps = self.left_cps_var.get()
                current_cps = self.get_randomized_cps(base_cps, self.left_random_var.get())

                # Calculate delay
                delay = 1.0 / current_cps

                # Perform click
                mouse_controller = mouse.Controller()
                mouse_controller.click(Button.left, 1)

                # Block hit chance
                if self.left_block_var.get() > 0:
                    if random.randint(1, 100) <= self.left_block_var.get():
                        time.sleep(0.05)  # Slight delay for block hit

                # Visual feedback
                if self.left_visual_var.get():
                    self.root.after(0, lambda: self.status_label.configure(text_color="green"))
                    self.root.after(100, lambda: self.status_label.configure(text_color="white"))

                time.sleep(delay)

            except Exception as e:
                self.log_status(f"Error in left click loop: {e}")
                time.sleep(0.1)

    def right_click_loop(self):
        """Right click autoclicker loop"""
        while self.running and self.right_click_active:
            try:
                # Check focus requirement
                if self.right_focus_var.get() and not self.is_minecraft_focused():
                    time.sleep(0.1)
                    continue

                # Get randomized CPS
                base_cps = self.right_cps_var.get()
                current_cps = self.get_randomized_cps(base_cps, self.right_random_var.get())

                # Calculate delay
                delay = 1.0 / current_cps

                # Perform click
                mouse_controller = mouse.Controller()
                mouse_controller.click(Button.right, 1)

                time.sleep(delay)

            except Exception as e:
                self.log_status(f"Error in right click loop: {e}")
                time.sleep(0.1)

    def toggle_left_click(self):
        """Toggle left click autoclicker"""
        if self.left_enable_var.get():
            if not self.left_click_active:
                self.left_click_active = True
                self.left_click_thread = threading.Thread(target=self.left_click_loop, daemon=True)
                self.left_click_thread.start()
                self.log_status("Left click autoclicker activated")
                self.update_status()
        else:
            self.left_click_active = False
            self.log_status("Left click autoclicker deactivated")
            self.update_status()

    def toggle_right_click(self):
        """Toggle right click autoclicker"""
        if self.right_enable_var.get():
            if not self.right_click_active:
                self.right_click_active = True
                self.right_click_thread = threading.Thread(target=self.right_click_loop, daemon=True)
                self.right_click_thread.start()
                self.log_status("Right click autoclicker activated")
                self.update_status()
        else:
            self.right_click_active = False
            self.log_status("Right click autoclicker deactivated")
            self.update_status()

    def update_left_cps(self, value):
        """Update left click CPS display"""
        self.left_cps_label.configure(text=f"CPS: {int(value)}")

    def update_right_cps(self, value):
        """Update right click CPS display"""
        self.right_cps_label.configure(text=f"CPS: {int(value)}")

    def update_status(self):
        """Update status display"""
        if self.left_click_active or self.right_click_active:
            status_text = "Status: Active"
            if self.left_click_active and self.right_click_active:
                status_text += " (Both)"
            elif self.left_click_active:
                status_text += " (Left)"
            else:
                status_text += " (Right)"
            self.status_label.configure(text=status_text, text_color="green")
        else:
            self.status_label.configure(text="Status: Inactive", text_color="white")

    def on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if button == Button.left and self.left_hold_var.get() and self.left_enable_var.get():
            if pressed and not self.left_click_active:
                self.left_click_active = True
                self.left_click_thread = threading.Thread(target=self.left_click_loop, daemon=True)
                self.left_click_thread.start()
                self.log_status("Left click hold activated")
                self.update_status()
            elif not pressed and self.left_click_active:
                self.left_click_active = False
                self.log_status("Left click hold deactivated")
                self.update_status()

        if button == Button.left and self.right_lmb_var.get() and self.right_enable_var.get():
            if pressed and not self.right_click_active:
                self.right_click_active = True
                self.right_click_thread = threading.Thread(target=self.right_click_loop, daemon=True)
                self.right_click_thread.start()
                self.log_status("Right click LMB lock activated")
                self.update_status()
            elif not pressed and self.right_click_active:
                self.right_click_active = False
                self.log_status("Right click LMB lock deactivated")
                self.update_status()

    def on_mouse_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events"""
        pass

    def on_key_press(self, key):
        """Handle key press events"""
        try:
            key_name = str(key).replace("Key.", "").lower()

            # Emergency stop
            if (hasattr(key, 'ctrl_l') or hasattr(key, 'ctrl_r')) and \
                    (hasattr(key, 'shift_l') or hasattr(key, 'shift_r')) and \
                    key == Key.end:
                self.emergency_stop()
                return

            # Hotkey handling
            if key_name == self.left_hotkey_var.get().lower():
                self.left_enable_var.set(not self.left_enable_var.get())
                self.toggle_left_click()
            elif key_name == self.right_hotkey_var.get().lower():
                self.right_enable_var.set(not self.right_enable_var.get())
                self.toggle_right_click()
            elif key_name == self.toggle_hotkey_var.get().lower():
                if self.root.winfo_viewable():
                    self.hide_window()
                else:
                    self.show_window()

        except Exception as e:
            self.log_status(f"Error handling key press: {e}")

    def on_key_release(self, key):
        """Handle key release events"""
        pass

    def log_status(self, message):
        """Log status message"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        def update_log():
            self.status_display.insert("end", log_message)
            self.status_display.see("end")

        if threading.current_thread() == threading.main_thread():
            update_log()
        else:
            self.root.after(0, update_log)

    def clear_status_log(self):
        """Clear status log"""
        self.status_display.delete("1.0", "end")

    def emergency_stop(self):
        """Emergency stop all functionality"""
        self.log_status("EMERGENCY STOP ACTIVATED!")

        # Stop all clicking
        self.left_click_active = False
        self.right_click_active = False
        self.left_enable_var.set(False)
        self.right_enable_var.set(False)

        # Update status
        self.update_status()

        # Self destruct if enabled
        if self.delete_config_var.get():
            self.self_destruct()

    def self_destruct(self):
        """Complete self destruct functionality"""
        self.log_status("SELF DESTRUCT INITIATED!")

        # Stop all threads
        self.running = False
        self.left_click_active = False
        self.right_click_active = False

        # Stop listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        # Remove system tray
        if self.tray_icon:
            self.tray_icon.stop()

        # Delete config file
        if os.path.exists(self.config_file):
            try:
                os.remove(self.config_file)
                self.log_status("Configuration file deleted")
            except:
                pass

        # Close GUI
        self.root.quit()
        self.root.destroy()

        # Force exit
        os._exit(0)

    def save_config(self):
        """Save configuration to file"""
        try:
            self.config["left_click"]["enabled"] = self.left_enable_var.get()
            self.config["left_click"]["cps"] = self.left_cps_var.get()
            self.config["left_click"]["randomization"] = self.left_random_var.get()
            self.config["left_click"]["hold_mode"] = self.left_hold_var.get()
            self.config["left_click"]["only_when_focused"] = self.left_focus_var.get()
            self.config["left_click"]["block_hit_chance"] = self.left_block_var.get()
            self.config["left_click"]["visual_feedback"] = self.left_visual_var.get()

            self.config["right_click"]["enabled"] = self.right_enable_var.get()
            self.config["right_click"]["cps"] = self.right_cps_var.get()
            self.config["right_click"]["randomization"] = self.right_random_var.get()
            self.config["right_click"]["lmb_lock"] = self.right_lmb_var.get()
            self.config["right_click"]["only_when_focused"] = self.right_focus_var.get()

            self.config["general"]["hotkey_left"] = self.left_hotkey_var.get()
            self.config["general"]["hotkey_right"] = self.right_hotkey_var.get()
            self.config["general"]["hotkey_toggle"] = self.toggle_hotkey_var.get()
            self.config["general"]["start_minimized"] = self.start_minimized_var.get()
            self.config["general"]["delete_config_on_exit"] = self.delete_config_var.get()

            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)

            self.log_status("Configuration saved successfully")

        except Exception as e:
            self.log_status(f"Error saving configuration: {e}")

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)

                # Update config with loaded values
                for section, values in loaded_config.items():
                    if section in self.config:
                        self.config[section].update(values)

                self.log_status("Configuration loaded successfully")
            else:
                self.log_status("No configuration file found, using defaults")

        except Exception as e:
            self.log_status(f"Error loading configuration: {e}")

    def show_window(self):
        """Show main window"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        """Hide main window to system tray"""
        self.root.withdraw()

    def quit_application(self):
        """Quit application"""
        self.running = False
        self.left_click_active = False
        self.right_click_active = False

        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.tray_icon:
            self.tray_icon.stop()

        self.root.quit()
        self.root.destroy()

    def on_closing(self):
        """Handle window closing"""
        if self.delete_config_var.get():
            self.self_destruct()
        else:
            self.hide_window()

    def run(self):
        """Start the application"""
        try:
            if self.config["general"]["start_minimized"]:
                self.root.withdraw()

            self.log_status("Minecraft AutoClicker started successfully")
            self.log_status("Press Ctrl+Shift+End for emergency stop")

            self.root.mainloop()

        except Exception as e:
            self.log_status(f"Error running application: {e}")
        finally:
            self.quit_application()

if __name__ == "__main__":
    try:
        app = MinecraftAutoClicker()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)