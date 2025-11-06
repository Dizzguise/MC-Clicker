
"""Main GUI application for MC Clicker using tkinter."""

import json
import os
import tkinter as tk
from tkinter import ttk

from src.clicker import AutoClicker
from src.hotkey import HotkeyManager
from src.utils import (
    cps_to_seconds,
    seconds_to_cps,
    validate_cps,
    validate_seconds,
)


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


class MCClickerApp:
    """Main application controller."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the application."""
        self.root = root
        self.root.title("MC Clicker")
        self.root.geometry("300x320")  # Compact, modern size
        self.root.resizable(False, False)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.setup_dark_theme()

        self.clicker = AutoClicker()
        self.hotkey_manager = HotkeyManager()

        # Settings
        self.cps: float = 1.6  # Changed from 10.0 to 1.6 (Minecraft friendly)
        self.button_type: str = "left"

        # Load saved hotkey
        saved_hotkey = self.load_hotkey()
        if saved_hotkey:
            self.hotkey_manager.set_hotkey(saved_hotkey)

        # Create GUI
        self.create_widgets()

        # Set initial clicker interval from CPS (FIX: Apply default CPS to clicker)
        self.clicker.set_interval(cps_to_seconds(self.cps))

        # Register hotkey callback
        self.hotkey_manager.register_callback(self.toggle_clicker)
        self.hotkey_manager.start_listening()

        # Update status periodically
        self.update_status()

        # Start the countdown update loop
        self.update_countdown()

        # Save hotkey on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_dark_theme(self) -> None:
        """Configure dark theme colors."""
        dark_bg = "#1e1e1e"
        dark_fg = "#ffffff"
        accent = "#0066cc"
        accent_hover = "#0080ff"
        border_color = "#3d3d3d"

        self.root.configure(bg=dark_bg)

        # Frame styling
        self.style.configure(
            "TFrame",
            background=dark_bg,
            foreground=dark_fg,
        )
        
        # Label styling
        self.style.configure(
            "TLabel",
            background=dark_bg,
            foreground=dark_fg,
        )
        
        # LabelFrame styling (important for section headers)
        self.style.configure(
            "TLabelframe",
            background=dark_bg,
            foreground=dark_fg,
            bordercolor=border_color,
            lightcolor=border_color,
            darkcolor=border_color,
        )
        self.style.configure(
            "TLabelframe.Label",
            background=dark_bg,
            foreground=dark_fg,
        )
        
        # Button styling
        self.style.configure(
            "TButton",
            background=accent,
            foreground=dark_fg,
            borderwidth=1,
        )
        self.style.map(
            "TButton",
            background=[("active", accent_hover), ("pressed", "#005ab3")],
            foreground=[("active", dark_fg)],
        )
        
        # Radio button styling
        self.style.configure(
            "TRadiobutton",
            background=dark_bg,
            foreground=dark_fg,
        )
        self.style.map(
            "TRadiobutton",
            background=[("active", dark_bg), ("pressed", dark_bg)],
        )
        
        # Entry styling
        self.style.configure(
            "TEntry",
            fieldbackground="#2d2d2d",
            background=dark_bg,
            foreground=dark_fg,
            borderwidth=1,
        )
        
        # Separator styling
        self.style.configure(
            "TSeparator",
            background=border_color,
        )

    def create_widgets(self) -> None:
        """Create the GUI widgets."""
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Header: Title + Status on same line
        header = ttk.Frame(main)
        header.pack(fill=tk.X, pady=(0, 8))

        title = ttk.Label(header, text="MC CLICKER", font=("Arial", 14, "bold"))
        title.pack(side=tk.LEFT)

        self.status_label = ttk.Label(
            header,
            text="STOPPED",
            font=("Arial", 11, "bold"),
            foreground="#ff6b6b",
        )
        self.status_label.pack(side=tk.RIGHT)

        # Countdown timer (hidden by default)
        self.countdown_label = ttk.Label(
            main,
            text="",
            font=("Arial", 9),
            foreground="#ffcc00",
        )
        self.countdown_label.pack(fill=tk.X, pady=(0, 6))

        # Click Speed: Single row
        speed_frame = ttk.Frame(main)
        speed_frame.pack(fill=tk.X, pady=4)
        ttk.Label(speed_frame, text="CPS:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.cps_var = tk.StringVar(value=f"{self.cps:.1f}")
        self.cps_entry = ttk.Entry(speed_frame, textvariable=self.cps_var, width=5)
        self.cps_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.cps_entry.bind("<KeyRelease>", self.on_cps_change)

        ttk.Label(speed_frame, text="Int:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.seconds_var = tk.StringVar(value=f"{cps_to_seconds(self.cps):.2f}s")
        self.seconds_entry = ttk.Entry(speed_frame, textvariable=self.seconds_var, width=5)
        self.seconds_entry.pack(side=tk.LEFT)
        self.seconds_entry.bind("<KeyRelease>", self.on_seconds_change)

        # Click Mode + Button: Single row
        mode_button_frame = ttk.Frame(main)
        mode_button_frame.pack(fill=tk.X, pady=4)

        ttk.Label(mode_button_frame, text="Mode:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.mode_var = tk.StringVar(value="click")
        ttk.Combobox(
            mode_button_frame,
            textvariable=self.mode_var,
            values=["Click", "Hold"],
            state="readonly",
            width=8,
        ).pack(side=tk.LEFT, padx=(0, 12))
        self.mode_var.trace("w", lambda *_: self.on_mode_change())

        ttk.Label(mode_button_frame, text="Button:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 4))
        self.button_var = tk.StringVar(value="left")
        ttk.Combobox(
            mode_button_frame,
            textvariable=self.button_var,
            values=["Left", "Right"],
            state="readonly",
            width=6,
        ).pack(side=tk.LEFT)
        self.button_var.trace("w", lambda *_: self.on_button_change())

        # Timer: Compact
        timer_frame = ttk.Frame(main)
        timer_frame.pack(fill=tk.X, pady=4)

        self.timer_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            timer_frame,
            text="Timer:",
            variable=self.timer_enabled_var,
            command=self.on_timer_toggle,
        ).pack(side=tk.LEFT, padx=(0, 4))

        self.timer_hours_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.timer_hours_var, width=2).pack(side=tk.LEFT)
        ttk.Label(timer_frame, text="h", font=("Arial", 8)).pack(side=tk.LEFT, padx=(0, 3))
        self.timer_hours_var.trace("w", self.on_timer_change)

        self.timer_minutes_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.timer_minutes_var, width=2).pack(side=tk.LEFT)
        ttk.Label(timer_frame, text="m", font=("Arial", 8)).pack(side=tk.LEFT, padx=(0, 3))
        self.timer_minutes_var.trace("w", self.on_timer_change)

        self.timer_seconds_var = tk.StringVar(value="0")
        ttk.Entry(timer_frame, textvariable=self.timer_seconds_var, width=2).pack(side=tk.LEFT)
        ttk.Label(timer_frame, text="s", font=("Arial", 8)).pack(side=tk.LEFT)

        # Hotkey: Compact
        hotkey_frame = ttk.Frame(main)
        hotkey_frame.pack(fill=tk.X, pady=4)

        ttk.Label(hotkey_frame, text="Hotkey:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 6))
        self.hotkey_label = ttk.Label(
            hotkey_frame,
            text=self.hotkey_manager.get_hotkey_display(),
            font=("Arial", 9, "bold"),
            foreground="#00ff00",
        )
        self.hotkey_label.pack(side=tk.LEFT, padx=(0, 8))

        self.record_button = ttk.Button(
            hotkey_frame,
            text="Change",
            command=self.start_recording_hotkey,
            width=8,
        )
        self.record_button.pack(side=tk.LEFT, padx=(0, 4))

        self.recording_label = ttk.Label(
            hotkey_frame,
            text="",
            font=("Arial", 8),
            foreground="#ff9900",
        )
        self.recording_label.pack(side=tk.LEFT)

        # Footer
        footer = ttk.Frame(main)
        footer.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(footer, text="Exit", command=self.exit_app, width=10).pack(side=tk.RIGHT)

    def on_cps_change(self, event: tk.Event = None) -> None:
        """Handle CPS input change."""
        try:
            cps = float(self.cps_var.get())
            if validate_cps(cps):
                self.cps = cps
                self.clicker.set_interval(cps_to_seconds(cps))
                self.seconds_var.set(f"{cps_to_seconds(cps):.2f}")
        except ValueError:
            pass

    def on_seconds_change(self, event: tk.Event = None) -> None:
        """Handle seconds input change."""
        try:
            seconds = float(self.seconds_var.get())
            if validate_seconds(seconds):
                cps = seconds_to_cps(seconds)
                self.cps = cps
                self.clicker.set_interval(seconds)
                self.cps_var.set(f"{cps:.1f}")
        except ValueError:
            pass

    def on_button_change(self) -> None:
        """Handle click button change."""
        button = self.button_var.get().lower()
        self.button_type = button
        self.clicker.set_button(button)

    def on_mode_change(self) -> None:
        """Handle click mode change."""
        mode = self.mode_var.get().lower()
        self.clicker.set_mode(mode)

    def on_timer_change(self, *args) -> None:
        """Handle timer input change (hours/minutes/seconds)."""
        if not self.timer_enabled_var.get():
            self.clicker.set_duration(None)
            return

        try:
            hours = int(self.timer_hours_var.get() or "0")
            minutes = int(self.timer_minutes_var.get() or "0")
            seconds = int(self.timer_seconds_var.get() or "0")

            total_seconds = hours * 3600 + minutes * 60 + seconds

            if total_seconds > 0:
                self.clicker.set_duration(total_seconds)
            else:
                self.clicker.set_duration(None)
        except ValueError:
            self.clicker.set_duration(None)

    def on_timer_toggle(self) -> None:
        """Handle timer enable/disable checkbox."""
        if self.timer_enabled_var.get():
            # Timer enabled, apply the values
            self.on_timer_change()
        else:
            # Timer disabled
            self.clicker.set_duration(None)
            self.countdown_label.config(text="")

    def update_countdown(self) -> None:
        """Update countdown display if timer is running."""
        remaining = self.clicker.get_remaining_time()

        if remaining is not None and self.timer_enabled_var.get():
            # Format remaining time
            hours = int(remaining // 3600)
            remaining %= 3600
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)

            countdown_text = f"Timer: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.countdown_label.config(text=countdown_text)
        else:
            self.countdown_label.config(text="")

        # Schedule next update
        self.root.after(100, self.update_countdown)

    def toggle_clicker(self) -> None:
        """Toggle the clicker on/off."""
        if self.clicker.is_running:
            self.clicker.stop()
        else:
            self.clicker.start()

    def start_clicker(self) -> None:
        """Start the clicker."""
        if not self.clicker.is_running:
            self.clicker.start()

    def stop_clicker(self) -> None:
        """Stop the clicker."""
        if self.clicker.is_running:
            self.clicker.stop()

    def exit_app(self) -> None:
        """Exit the application."""
        self.clicker.stop()
        self.hotkey_manager.stop_listening()
        self.root.destroy()

    def update_status(self) -> None:
        """Update status display periodically."""
        if self.clicker.is_running:
            self.status_label.config(text="RUNNING", foreground="#51cf66")
        else:
            self.status_label.config(text="STOPPED", foreground="#ff6b6b")

        # Schedule next update
        self.root.after(100, self.update_status)

    def start_recording_hotkey(self) -> None:
        """Start the hotkey recording process."""
        self.record_button.config(state=tk.DISABLED)
        self.recording_label.pack(side=tk.LEFT, padx=10)
        self.recording_label.config(text="Press a key...")
        self.root.bind("<KeyPress>", self.on_hotkey_key_press)
        self.recording_keys = set()
        self.root.focus()

    def on_hotkey_key_press(self, event: tk.Event) -> None:
        """Record key press and auto-save."""
        if event.keysym not in self.recording_keys:
            self.recording_keys.add(event.keysym)
            self.update_recording_display()
            # Auto-save after recording keys
            self.root.after(100, self.auto_save_hotkey)

    def on_hotkey_key_release(self, event: tk.Event) -> None:
        """Handle key release."""
        self.recording_keys.discard(event.keysym)

    def update_recording_display(self) -> None:
        """Update the display with current key combination."""
        if not self.recording_keys:
            self.recording_label.config(text="Press a key...")
            return

        # Map tkinter key names to friendly names
        key_map = {
            "Control_L": "ctrl", "Control_R": "ctrl",
            "Shift_L": "shift", "Shift_R": "shift",
            "Alt_L": "alt", "Alt_R": "alt",
        }

        display_keys = []
        for key in sorted(self.recording_keys):
            friendly_key = key_map.get(key, key.lower())
            if friendly_key not in display_keys:
                display_keys.append(friendly_key)

        display_text = "+".join(display_keys)
        self.recording_label.config(text=display_text)

    def auto_save_hotkey(self) -> None:
        """Auto-save the hotkey after keys are pressed."""
        if not self.recording_keys:
            return

        # Convert to hotkey format
        key_map = {
            "Control_L": "ctrl", "Control_R": "ctrl",
            "Shift_L": "shift", "Shift_R": "shift",
            "Alt_L": "alt", "Alt_R": "alt",
        }

        keys = []
        for key in sorted(self.recording_keys):
            friendly_key = key_map.get(key, key.lower())
            if friendly_key not in keys:
                keys.append(friendly_key)

        new_hotkey = "+".join(keys)

        # Stop old listener
        self.hotkey_manager.stop_listening()

        # Set new hotkey
        self.hotkey_manager.set_hotkey(HotkeyManager.parse_hotkey_input(new_hotkey))

        # Start new listener
        self.hotkey_manager.start_listening()

        # Update display
        self.hotkey_label.config(text=f"Current: {self.hotkey_manager.get_hotkey_display()}")

        # Reset UI
        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")
        self.record_button.config(state=tk.NORMAL)
        self.recording_label.config(text="")
        self.recording_label.pack_forget()
        self.record_button.pack(side=tk.LEFT, padx=5)

    def finish_recording_hotkey(self) -> None:
        """Finish the hotkey recording process (kept for compatibility)."""
        pass

    def load_hotkey(self) -> str | None:
        """Load the hotkey from a config file."""
        if not os.path.exists(CONFIG_FILE):
            return None

        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return HotkeyManager.parse_hotkey_input(data.get("hotkey", ""))
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {CONFIG_FILE}")
            return None
        except Exception as e:
            print(f"Error loading hotkey from {CONFIG_FILE}: {e}")
            return None

    def on_close(self) -> None:
        """Save hotkey and exit."""
        self.save_hotkey()
        self.exit_app()

    def save_hotkey(self) -> None:
        """Save the current hotkey to a config file."""
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"hotkey": self.hotkey_manager.get_hotkey_display()}, f)
        except Exception as e:
            print(f"Error saving hotkey to {CONFIG_FILE}: {e}")


def main() -> None:
    """Entry point for the application."""
    root = tk.Tk()
    app = MCClickerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
