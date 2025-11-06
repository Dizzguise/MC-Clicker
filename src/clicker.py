
"""Mouse clicking logic for MC Clicker."""

import threading
import time
from typing import Literal

from pynput.mouse import Button, Controller


class AutoClicker:
    """Handles automated mouse clicking."""

    def __init__(self) -> None:
        """Initialize the AutoClicker."""
        self.mouse = Controller()
        self.is_running: bool = False
        self.is_holding: bool = False  # Track if button is currently held
        self.click_thread: threading.Thread | None = None
        self.interval: float = 0.1  # Default 10 CPS
        self.button: Button = Button.left
        self.mode: Literal["click", "hold"] = "click"  # "click" or "hold"
        self.duration: float | None = None  # Duration in seconds, None = infinite
        self.start_time: float | None = None

    def set_interval(self, interval: float) -> None:
        """
        Set the interval between clicks in seconds.

        Args:
            interval (float): Seconds between clicks.
        """
        if interval <= 0:
            raise ValueError("Interval must be greater than 0")
        self.interval = interval

    def set_button(self, button_type: Literal["left", "right"]) -> None:
        """
        Set the mouse button to click.

        Args:
            button_type (Literal["left", "right"]): Button type to use.

        Raises:
            ValueError: If button_type is not 'left' or 'right'.
        """
        if button_type == "left":
            self.button = Button.left
        elif button_type == "right":
            self.button = Button.right
        else:
            raise ValueError(f"Invalid button type: {button_type}")

    def set_mode(self, mode: Literal["click", "hold"]) -> None:
        """
        Set the clicking mode.

        Args:
            mode (Literal["click", "hold"]): "click" for regular clicking, "hold" for click-and-hold.
        """
        if mode not in ["click", "hold"]:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode

    def set_duration(self, duration: float | None) -> None:
        """
        Set the duration to run in seconds.

        Args:
            duration (float | None): Duration in seconds, None for infinite.
        """
        if duration is not None and duration <= 0:
            raise ValueError("Duration must be greater than 0")
        self.duration = duration

    def _click_loop(self) -> None:
        """Internal loop for continuous clicking."""
        self.start_time = time.time()

        while self.is_running:
            # Check if duration exceeded
            if self.duration is not None:
                elapsed = time.time() - self.start_time
                if elapsed >= self.duration:
                    self.is_running = False
                    # Release button if in hold mode
                    if self.is_holding:
                        self.mouse.release(self.button)
                        self.is_holding = False
                    break

            try:
                if self.mode == "hold":
                    # For hold mode: press and stay held
                    if not self.is_holding:
                        self.mouse.press(self.button)
                        self.is_holding = True
                    time.sleep(0.01)  # Small sleep to prevent CPU spinning
                else:
                    # Regular click mode
                    self.mouse.click(self.button, 1)
                    time.sleep(self.interval)
            except Exception as e:
                print(f"Click error: {e}")
                break

    def start(self) -> None:
        """Start the auto-clicker."""
        if self.is_running:
            return  # Already running

        self.is_running = True
        self.click_thread = threading.Thread(target=self._click_loop, daemon=True)
        self.click_thread.start()

    def stop(self) -> None:
        """Stop the auto-clicker."""
        self.is_running = False
        # Release button if it's held
        if self.is_holding:
            try:
                self.mouse.release(self.button)
                self.is_holding = False
            except Exception as e:
                print(f"Release error: {e}")
        if self.click_thread:
            self.click_thread.join(timeout=1) 

    def get_remaining_time(self) -> float | None:
        """
        Get remaining time in seconds.

        Returns:
            float | None: Remaining seconds, or None if not running or no duration set.
        """
        if not self.is_running or self.duration is None or self.start_time is None:
            return None
        
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining) 