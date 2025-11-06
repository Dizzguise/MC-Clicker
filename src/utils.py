
"""Utility functions for MC Clicker."""

from typing import Union


def cps_to_seconds(cps: Union[int, float]) -> float:
    """
    Convert clicks per second (CPS) to seconds between clicks.

    Args:
        cps (Union[int, float]): Clicks per second (0.1 to 100).

    Returns:
        float: Seconds between clicks.
    """
    if cps <= 0:
        raise ValueError("CPS must be greater than 0")
    return 1.0 / cps


def seconds_to_cps(seconds: Union[int, float]) -> float:
    """
    Convert seconds between clicks to clicks per second (CPS).

    Args:
        seconds (Union[int, float]): Seconds between clicks.

    Returns:
        float: Clicks per second.
    """
    if seconds <= 0:
        raise ValueError("Seconds must be greater than 0")
    return 1.0 / seconds


def validate_cps(cps: Union[int, float]) -> bool:
    """
    Validate CPS value (0.1 to 100).

    Args:
        cps (Union[int, float]): CPS value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return 0.1 <= cps <= 100


def validate_seconds(seconds: Union[int, float]) -> bool:
    """
    Validate seconds value (must result in 0.1-100 CPS).

    Args:
        seconds (Union[int, float]): Seconds value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if seconds <= 0:
        return False
    cps = seconds_to_cps(seconds)
    return validate_cps(cps)


def parse_timer_input(time_str: str) -> float | None:
    """
    Parse timer input string to seconds.

    Examples: "30s" = 30 seconds, "5m" = 300 seconds, "1h" = 3600 seconds
    "1h30m" = 5400 seconds

    Args:
        time_str (str): Timer string (e.g., "30s", "5m", "1h", "1h30m15s")

    Returns:
        float | None: Total seconds, or None if invalid format.
    """
    if not time_str or not time_str.strip():
        return None

    time_str = time_str.lower().strip().replace(" ", "")
    total_seconds = 0

    # Parse hours
    if "h" in time_str:
        parts = time_str.split("h")
        try:
            hours = float(parts[0])
            total_seconds += hours * 3600
            time_str = parts[1]
        except (ValueError, IndexError):
            return None

    # Parse minutes
    if "m" in time_str:
        parts = time_str.split("m")
        try:
            minutes = float(parts[0])
            total_seconds += minutes * 60
            time_str = parts[1]
        except (ValueError, IndexError):
            return None

    # Parse seconds
    if "s" in time_str:
        parts = time_str.split("s")
        try:
            seconds = float(parts[0])
            total_seconds += seconds
        except (ValueError, IndexError):
            return None
    elif time_str:  # Remaining text that's not parsed
        return None

    return total_seconds if total_seconds > 0 else None


def format_time_display(seconds: float) -> str:
    """
    Format seconds to display format.

    Args:
        seconds (float): Total seconds.

    Returns:
        str: Formatted time string (e.g., "1h 30m 45s").
    """
    hours = int(seconds // 3600)
    remaining = seconds % 3600
    minutes = int(remaining // 60)
    secs = int(remaining % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)

