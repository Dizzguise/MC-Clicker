
"""Unit tests for utils module."""

import pytest

from src.utils import (
    cps_to_seconds,
    seconds_to_cps,
    validate_cps,
    validate_seconds,
)


class TestCpsToSeconds:
    """Tests for CPS to seconds conversion."""

    def test_10_cps_to_seconds(self) -> None:
        """Test converting 10 CPS to 0.1 seconds."""
        assert cps_to_seconds(10) == 0.1

    def test_5_cps_to_seconds(self) -> None:
        """Test converting 5 CPS to 0.2 seconds."""
        assert cps_to_seconds(5) == 0.2

    def test_100_cps_to_seconds(self) -> None:
        """Test converting 100 CPS to 0.01 seconds."""
        assert cps_to_seconds(100) == 0.01

    def test_cps_to_seconds_invalid_zero(self) -> None:
        """Test that 0 CPS raises ValueError."""
        with pytest.raises(ValueError):
            cps_to_seconds(0)

    def test_cps_to_seconds_invalid_negative(self) -> None:
        """Test that negative CPS raises ValueError."""
        with pytest.raises(ValueError):
            cps_to_seconds(-5)


class TestSecondsToCps:
    """Tests for seconds to CPS conversion."""

    def test_0_1_seconds_to_cps(self) -> None:
        """Test converting 0.1 seconds to 10 CPS."""
        assert seconds_to_cps(0.1) == 10

    def test_0_2_seconds_to_cps(self) -> None:
        """Test converting 0.2 seconds to 5 CPS."""
        assert seconds_to_cps(0.2) == 5

    def test_1_second_to_cps(self) -> None:
        """Test converting 1 second to 1 CPS."""
        assert seconds_to_cps(1) == 1

    def test_seconds_to_cps_invalid_zero(self) -> None:
        """Test that 0 seconds raises ValueError."""
        with pytest.raises(ValueError):
            seconds_to_cps(0)

    def test_seconds_to_cps_invalid_negative(self) -> None:
        """Test that negative seconds raises ValueError."""
        with pytest.raises(ValueError):
            seconds_to_cps(-1)


class TestValidateCps:
    """Tests for CPS validation."""

    def test_valid_cps_low(self) -> None:
        """Test valid CPS at lower bound (0.1)."""
        assert validate_cps(0.1) is True

    def test_valid_cps_high(self) -> None:
        """Test valid CPS at upper bound (100)."""
        assert validate_cps(100) is True

    def test_valid_cps_mid(self) -> None:
        """Test valid CPS in middle of range."""
        assert validate_cps(10) is True

    def test_invalid_cps_too_low(self) -> None:
        """Test CPS below minimum is invalid."""
        assert validate_cps(0.05) is False

    def test_invalid_cps_too_high(self) -> None:
        """Test CPS above maximum is invalid."""
        assert validate_cps(101) is False

    def test_invalid_cps_zero(self) -> None:
        """Test CPS of 0 is invalid."""
        assert validate_cps(0) is False


class TestValidateSeconds:
    """Tests for seconds validation."""

    def test_valid_seconds_0_1(self) -> None:
        """Test 0.1 seconds (100 CPS) is valid."""
        assert validate_seconds(0.01) is True  # 100 CPS

    def test_valid_seconds_10(self) -> None:
        """Test 10 seconds (0.1 CPS) is valid."""
        assert validate_seconds(10) is True

    def test_invalid_seconds_too_low(self) -> None:
        """Test seconds resulting in >100 CPS is invalid."""
        assert validate_seconds(0.005) is False  # 200 CPS

    def test_invalid_seconds_too_high(self) -> None:
        """Test seconds resulting in <0.1 CPS is invalid."""
        assert validate_seconds(11) is False

    def test_invalid_seconds_zero(self) -> None:
        """Test 0 seconds is invalid."""
        assert validate_seconds(0) is False

