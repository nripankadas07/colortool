"""Core Color class and color manipulation logic."""
from typing import Tuple


class ColorError(Exception):
    """Exception raised for color-related errors."""

    pass


class Color:
    """Immutable color object supporting HEX, RGB, and HSL formats."""

    def __init__(self, red: int, green: int, blue: int) -> None:
        """Initialize Color with RGB values (0-255).

        Args:
            red: Red component (0-255)
            green: Green component (0-255)
            blue: Blue component (0-255)

        Raises:
            ColorError: If RGB values are out of range
        """
        if not all(0 <= val <= 255 for val in [red, green, blue]):
            raise ColorError("RGB values must be between 0 and 255")
        self._red = red
        self._green = green
        self._blue = blue

    @classmethod
    def from_hex(cls, hex_string: str) -> "Color":
        """Create Color from hexadecimal string.

        Args:
            hex_string: Hex color string like "#FF5733" or "FF5733"
                       Supports both 3-char (#RGB) and 6-char (#RRGGBB) formats

        Returns:
            Color instance

        Raises:
            ColorError: If hex string is invalid
        """
        if not hex_string:
            raise ColorError("Hex string cannot be empty")

        hex_str = hex_string.lstrip("#").upper()
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        elif len(hex_str) != 6:
            raise ColorError(f"Hex must be 3 or 6 chars (got {len(hex_str)})")

        if not all(c in "0123456789ABCDEF" for c in hex_str):
            raise ColorError(f"Invalid hex characters: '{hex_str}'")

        try:
            return cls(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))
        except ValueError as e:
            raise ColorError(f"Failed to parse hex: {e}")

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int) -> "Color":
        """Create Color from RGB values.

        Args:
            red: Red component (0-255)
            green: Green component (0-255)
            blue: Blue component (0-255)

        Returns:
            Color instance

        Raises:
            ColorError: If RGB values are out of range
        """
        return cls(red, green, blue)

    @classmethod
    def from_hsl(cls, hue: float, saturation: float, lightness: float) -> "Color":
        """Create Color from HSL values.

        Args:
            hue: Hue (0-360 degrees)
            saturation: Saturation (0-1)
            lightness: Lightness (0-1)

        Returns:
            Color instance

        Raises:
            ColorError: If HSL values are out of range
        """
        if not 0 <= hue <= 360:
            raise ColorError(f"Hue must be between 0 and 360 (got {hue})")
        if not 0 <= saturation <= 1:
            raise ColorError(
                f"Saturation must be between 0 and 1 (got {saturation})"
            )
        if not 0 <= lightness <= 1:
            raise ColorError(
                f"Lightness must be between 0 and 1 (got {lightness})"
            )

        red, green, blue = _hsl_to_rgb(hue, saturation, lightness)
        return cls(red, green, blue)

    def to_hex(self) -> str:
        """Convert to hexadecimal string format.

        Returns:
            Hex string in format "#RRGGBB" (uppercase)
        """
        return f"#{self._red:02X}{self._green:02X}{self._blue:02X}"

    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple.

        Returns:
            Tuple of (red, green, blue) with values 0-255
        """
        return (self._red, self._green, self._blue)

    def to_hsl(self) -> Tuple[float, float, float]:
        """Convert to HSL tuple.

        Returns:
            Tuple of (hue, saturation, lightness)
            hue: 0-360 degrees
            saturation: 0-1
            lightness: 0-1
        """
        return _rgb_to_hsl(self._red, self._green, self._blue)

    def lighten(self, amount: float) -> "Color":
        """Return a lighter color by increasing lightness.

        Args:
            amount: Amount to increase lightness (0-1)

        Returns:
            New Color instance
        """
        h, s, l = self.to_hsl()
        new_l = min(1.0, l + amount)
        return Color.from_hsl(h, s, new_l)

    def darken(self, amount: float) -> "Color":
        """Return a darker color by decreasing lightness.

        Args:
            amount: Amount to decrease lightness (0-1)

        Returns:
            New Color instance
        """
        h, s, l = self.to_hsl()
        new_l = max(0.0, l - amount)
        return Color.from_hsl(h, s, new_l)

    def saturate(self, amount: float) -> "Color":
        """Return a more saturated color.

        Args:
            amount: Amount to increase saturation (0-1)

        Returns:
            New Color instance
        """
        h, s, l = self.to_hsl()
        new_s = min(1.0, s + amount)
        return Color.from_hsl(h, new_s, l)

    def desaturate(self, amount: float) -> "Color":
        """Return a less saturated color.

        Args:
            amount: Amount to decrease saturation (0-1)

        Returns:
            New Color instance
        """
        h, s, l = self.to_hsl()
        new_s = max(0.0, s - amount)
        return Color.from_hsl(h, new_s, l)

    def complement(self) -> "Color":
        """Return the complementary color (hue rotated 180 degrees).

        Returns:
            New Color instance
        """
        h, s, l = self.to_hsl()
        new_h = (h + 180) % 360
        return Color.from_hsl(new_h, s, l)

    def mix(self, other: "Color", weight: float) -> "Color":
        """Mix this color with another color.

        Args:
            other: Another Color instance
            weight: Weight of the other color (0-1).
                   0 returns this color, 1 returns other color

        Returns:
            New Color instance

        Raises:
            ColorError: If weight is not in range [0, 1]
        """
        if not 0 <= weight <= 1:
            raise ColorError(f"Mix weight must be between 0 and 1 (got {weight})")

        r1, g1, b1 = self.to_rgb()
        r2, g2, b2 = other.to_rgb()

        red = int(r1 * (1 - weight) + r2 * weight)
        green = int(g1 * (1 - weight) + g2 * weight)
        blue = int(b1 * (1 - weight) + b2 * weight)

        return Color.from_rgb(red, green, blue)

    def __repr__(self) -> str:
        """Return string representation of Color."""
        return f"Color({self.to_hex()})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on RGB values."""
        if not isinstance(other, Color):
            return NotImplemented
        return self.to_rgb() == other.to_rgb()

    def __hash__(self) -> int:
        """Make Color hashable."""
        return hash(self.to_rgb())


def _rgb_to_hsl(red: int, green: int, blue: int) -> Tuple[float, float, float]:
    """Convert RGB to HSL.

    Args:
        red: 0-255
        green: 0-255
        blue: 0-255

    Returns:
        Tuple of (hue, saturation, lightness)
    """
    r, g, b = red / 255.0, green / 255.0, blue / 255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2.0

    if max_c == min_c:
        return (0.0, 0.0, l)

    d = max_c - min_c
    s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)

    if max_c == r:
        h = (g - b) / d + (6.0 if g < b else 0.0)
    elif max_c == g:
        h = (b - r) / d + 2.0
    else:
        h = (r - g) / d + 4.0

    return ((h / 6.0) * 360.0, s, l)


def _hue_to_rgb(p: float, q: float, t: float) -> float:
    """Convert hue component to RGB value.

    Args:
        p: First interpolation value
        q: Second interpolation value
        t: Normalized hue segment

    Returns:
        RGB component value (0-1)
    """
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6.0:
        return p + (q - p) * 6.0 * t
    if t < 1 / 2.0:
        return q
    if t < 2 / 3.0:
        return p + (q - p) * (2 / 3.0 - t) * 6.0
    return p


def _hsl_to_rgb(hue: float, saturation: float, lightness: float) -> Tuple[int, int, int]:
    """Convert HSL to RGB.

    Args:
        hue: 0-360 degrees
        saturation: 0-1
        lightness: 0-1

    Returns:
        Tuple of (red, green, blue) with values 0-255
    """
    h = hue / 360.0
    s = saturation
    l = lightness

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = _hue_to_rgb(p, q, h + 1 / 3.0)
        g = _hue_to_rgb(p, q, h)
        b = _hue_to_rgb(p, q, h - 1 / 3.0)

    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))
