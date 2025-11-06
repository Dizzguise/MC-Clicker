
"""Hotkey management for MC Clicker."""

import threading
from typing import Callable

import keyboard


class HotkeyManager:
    """Manages hotkey registration and detection."""

    def __init__(self) -> None:
        """Initialize the HotkeyManager."""
        self.hotkey: str = "f6"
        self.callback: Callable[[], None] | None = None
        self.is_listening: bool = False
        self.listener_thread: threading.Thread | None = None

    def set_hotkey(self, hotkey: str) -> None:
        """
        Set the hotkey string.

        Args:
            hotkey (str): Hotkey string (e.g., 'f6', 'ctrl+f6', 'alt+shift+f6').

        Reason:
            Hotkey format is library-specific. keyboard library uses '+' to separate
            modifiers from the main key, with '+' also used for combinations.
        """
        self.hotkey = hotkey.lower()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """
        Register a callback function to execute when hotkey is pressed.

        Args:
            callback (Callable[[], None]): Function to call on hotkey press.
        """
        self.callback = callback

    def start_listening(self) -> None:
        """Start listening for hotkey presses."""
        if self.is_listening:
            return  # Already listening

        try:
            keyboard.add_hotkey(self.hotkey, self._on_hotkey_press)
            self.is_listening = True
        except ValueError as e:
            print(f"Invalid hotkey '{self.hotkey}': {e}")

    def stop_listening(self) -> None:
        """Stop listening for hotkey presses."""
        if not self.is_listening:
            return

        try:
            keyboard.remove_hotkey(self.hotkey)
            self.is_listening = False
        except ValueError:
            pass  # Hotkey might not be registered

    def _on_hotkey_press(self) -> None:
        """Internal callback when hotkey is pressed."""
        if self.callback:
            self.callback()

    def get_hotkey_display(self) -> str:
        """
        Get formatted hotkey string for display.

        Returns:
            str: Display-friendly hotkey string (uppercase first letter).
        """
        return self.hotkey.replace("+", " + ").upper()

    @staticmethod
    def parse_hotkey_input(key_str: str) -> str:
        """
        Parse user input to valid hotkey string.

        Args:
            key_str (str): User input hotkey string.

        Returns:
            str: Normalized hotkey string.
        """
        # Simple normalization: lowercase, strip spaces, validate
        normalized = key_str.lower().replace(" ", "").strip()
        if not normalized:
            return "f6"  # Default fallback
        return normalized 