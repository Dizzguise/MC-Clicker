
"""Unit tests for hotkey module."""

import pytest

from src.hotkey import HotkeyManager


class TestHotkeyManagerInitialization:
    """Tests for HotkeyManager initialization."""

    def test_init_defaults(self) -> None:
        """Test HotkeyManager initializes with correct defaults."""
        manager = HotkeyManager()
        assert manager.hotkey == "f6"
        assert manager.callback is None
        assert manager.is_listening is False

    def test_init_hotkey_lowercase(self) -> None:
        """Test that default hotkey is lowercase."""
        manager = HotkeyManager()
        assert manager.hotkey == "f6"


class TestSetHotkey:
    """Tests for setting hotkey."""

    def test_set_hotkey_single_key(self) -> None:
        """Test setting a single key hotkey."""
        manager = HotkeyManager()
        manager.set_hotkey("f7")
        assert manager.hotkey == "f7"

    def test_set_hotkey_with_modifier(self) -> None:
        """Test setting hotkey with modifier."""
        manager = HotkeyManager()
        manager.set_hotkey("ctrl+f7")
        assert manager.hotkey == "ctrl+f7"

    def test_set_hotkey_uppercase_normalized(self) -> None:
        """Test that uppercase hotkey is normalized to lowercase."""
        manager = HotkeyManager()
        manager.set_hotkey("CTRL+F7")
        assert manager.hotkey == "ctrl+f7"

    def test_set_hotkey_multiple_modifiers(self) -> None:
        """Test setting hotkey with multiple modifiers."""
        manager = HotkeyManager()
        manager.set_hotkey("alt+shift+f8")
        assert manager.hotkey == "alt+shift+f8"


class TestRegisterCallback:
    """Tests for callback registration."""

    def test_register_callback(self) -> None:
        """Test registering a callback function."""
        manager = HotkeyManager()

        def dummy_callback() -> None:
            pass

        manager.register_callback(dummy_callback)
        assert manager.callback is dummy_callback

    def test_replace_callback(self) -> None:
        """Test replacing an existing callback."""
        manager = HotkeyManager()

        def callback1() -> None:
            pass

        def callback2() -> None:
            pass

        manager.register_callback(callback1)
        manager.register_callback(callback2)
        assert manager.callback is callback2


class TestGetHotkeyDisplay:
    """Tests for display formatting."""

    def test_display_single_key(self) -> None:
        """Test display format for single key."""
        manager = HotkeyManager()
        manager.set_hotkey("f6")
        assert manager.get_hotkey_display() == "F6"

    def test_display_with_modifier(self) -> None:
        """Test display format with modifier."""
        manager = HotkeyManager()
        manager.set_hotkey("ctrl+f6")
        assert manager.get_hotkey_display() == "CTRL + F6"

    def test_display_multiple_modifiers(self) -> None:
        """Test display format with multiple modifiers."""
        manager = HotkeyManager()
        manager.set_hotkey("alt+shift+f8")
        assert manager.get_hotkey_display() == "ALT + SHIFT + F8"


class TestParseHotkeyInput:
    """Tests for input parsing."""

    def test_parse_simple_key(self) -> None:
        """Test parsing simple key."""
        result = HotkeyManager.parse_hotkey_input("f7")
        assert result == "f7"

    def test_parse_with_spaces(self) -> None:
        """Test parsing removes spaces."""
        result = HotkeyManager.parse_hotkey_input("ctrl + f7")
        assert result == "ctrl+f7"

    def test_parse_uppercase_normalized(self) -> None:
        """Test parsing normalizes to lowercase."""
        result = HotkeyManager.parse_hotkey_input("CTRL+F7")
        assert result == "ctrl+f7"

    def test_parse_empty_returns_default(self) -> None:
        """Test that empty string returns default."""
        result = HotkeyManager.parse_hotkey_input("")
        assert result == "f6"

    def test_parse_only_spaces_returns_default(self) -> None:
        """Test that only spaces returns default."""
        result = HotkeyManager.parse_hotkey_input("   ")
        assert result == "f6"


class TestListening:
    """Tests for listener control."""

    def test_stop_when_not_listening(self) -> None:
        """Test stopping when not listening is safe."""
        manager = HotkeyManager()
        manager.stop_listening()  # Should not raise exception

    def test_double_start_listening(self) -> None:
        """Test that starting twice doesn't duplicate listeners."""
        manager = HotkeyManager()
        manager.start_listening()
        manager.start_listening()  # Should not create duplicate
        assert manager.is_listening is True
        manager.stop_listening()

