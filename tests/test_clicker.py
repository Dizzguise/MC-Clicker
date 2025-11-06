
"""Unit tests for clicker module."""

import time

import pytest

from src.clicker import AutoClicker


class TestAutoClickerInitialization:
    """Tests for AutoClicker initialization."""

    def test_init_defaults(self) -> None:
        """Test AutoClicker initializes with correct defaults."""
        clicker = AutoClicker()
        assert clicker.is_running is False
        assert clicker.interval == 0.1
        assert clicker.click_thread is None

    def test_init_not_running(self) -> None:
        """Test AutoClicker is not running on initialization."""
        clicker = AutoClicker()
        assert clicker.is_running is False


class TestSetInterval:
    """Tests for interval setting."""

    def test_set_interval_valid(self) -> None:
        """Test setting a valid interval."""
        clicker = AutoClicker()
        clicker.set_interval(0.2)
        assert clicker.interval == 0.2

    def test_set_interval_zero_raises_error(self) -> None:
        """Test that zero interval raises ValueError."""
        clicker = AutoClicker()
        with pytest.raises(ValueError):
            clicker.set_interval(0)

    def test_set_interval_negative_raises_error(self) -> None:
        """Test that negative interval raises ValueError."""
        clicker = AutoClicker()
        with pytest.raises(ValueError):
            clicker.set_interval(-0.1)


class TestSetButton:
    """Tests for button selection."""

    def test_set_button_left(self) -> None:
        """Test setting left button."""
        clicker = AutoClicker()
        clicker.set_button("left")
        # Just verify no exception is raised

    def test_set_button_right(self) -> None:
        """Test setting right button."""
        clicker = AutoClicker()
        clicker.set_button("right")
        # Just verify no exception is raised

    def test_set_button_invalid_raises_error(self) -> None:
        """Test that invalid button raises ValueError."""
        clicker = AutoClicker()
        with pytest.raises(ValueError):
            clicker.set_button("middle")


class TestStartStop:
    """Tests for start/stop functionality."""

    def test_start_sets_running(self) -> None:
        """Test that start() sets is_running to True."""
        clicker = AutoClicker()
        clicker.start()
        assert clicker.is_running is True
        clicker.stop()

    def test_stop_clears_running(self) -> None:
        """Test that stop() sets is_running to False."""
        clicker = AutoClicker()
        clicker.start()
        assert clicker.is_running is True
        clicker.stop()
        time.sleep(0.2)  # Wait for thread to stop
        assert clicker.is_running is False

    def test_double_start_safe(self) -> None:
        """Test that calling start twice is safe."""
        clicker = AutoClicker()
        clicker.start()
        thread1 = clicker.click_thread
        clicker.start()
        thread2 = clicker.click_thread
        # Should be same thread (not create a new one)
        assert thread1 is thread2
        clicker.stop()

    def test_stop_when_not_running_safe(self) -> None:
        """Test that stop when not running is safe."""
        clicker = AutoClicker()
        clicker.stop()  # Should not raise exception

