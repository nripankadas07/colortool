"""Comprehensive test suite for colortool Color class."""
import pytest
from colortool import Color, ColorError


class TestColorConstruction:
    """Test Color object construction from various formats."""

    def test_from_hex_with_hash_six_char(self):
        """Test parsing 6-character hex with hash prefix."""
        color = Color.from_hex("#FF5733")
        assert color.to_rgb() == (255, 87, 51)

    def test_from_hex_without_hash_six_char(self):
        """Test parsing 6-character hex without hash prefix."""
        color = Color.from_hex("FF5733")
        assert color.to_rgb() == (255, 87, 51)

    def test_from_hex_three_char_shorthand(self):
        """Test parsing 3-character hex shorthand (e.g., #F0A)."""
        color = Color.from_hex("#F0A")
        # #F0A should expand to #FF00AA
        assert color.to_rgb() == (255, 0, 170)

    def test_from_hex_lowercase(self):
        """Test case-insensitivity for hex parsing."""
        color = Color.from_hex("#ff5733")
        assert color.to_rgb() == (255, 87, 51)

    def test_from_hex_mixed_case(self):
        """Test mixed-case hex parsing."""
        color = Color.from_hex("#Ff57Ab")
        assert color.to_rgb() == (255, 87, 171)

    def test_from_hex_invalid_length(self):
        """Test error on invalid hex length."""
        with pytest.raises(ColorError):
            Color.from_hex("#FF57")

    def test_from_hex_invalid_chars(self):
        """Test error on invalid hex characters."""
        with pytest.raises(ColorError):
            Color.from_hex("#GGHHII")

    def test_from_hex_empty_string(self):
        """Test error on empty string."""
        with pytest.raises(ColorError):
            Color.from_hex("")

    def test_from_rgb_valid(self):
        """Test RGB construction with valid values."""
        color = Color.from_rgb(255, 87, 51)
        assert color.to_rgb() == (255, 87, 51)

    def test_from_rgb_black(self):
        """Test RGB construction for black."""
        color = Color.from_rgb(0, 0, 0)
        assert color.to_rgb() == (0, 0, 0)

    def test_from_rgb_white(self):
        """Test RGB construction for white."""
        color = Color.from_rgb(255, 255, 255)
        assert color.to_rgb() == (255, 255, 255)

    def test_from_rgb_out_of_range_high(self):
        """Test error on RGB value > 255."""
        with pytest.raises(ColorError):
            Color.from_rgb(256, 100, 100)

    def test_from_rgb_out_of_range_low(self):
        """Test error on RGB value < 0."""
        with pytest.raises(ColorError):
            Color.from_rgb(-1, 100, 100)

    def test_from_hsl_valid(self):
        """Test HSL construction with valid values."""
        color = Color.from_hsl(120, 1.0, 0.5)
        # Pure green
        r, g, b = color.to_rgb()
        assert g > r and g > b  # Green should dominate

    def test_from_hsl_black(self):
        """Test HSL construction for black (L=0)."""
        color = Color.from_hsl(0, 0, 0)
        assert color.to_rgb() == (0, 0, 0)

    def test_from_hsl_white(self):
        """Test HSL construction for white (L=1)."""
        color = Color.from_hsl(0, 0, 1)
        assert color.to_rgb() == (255, 255, 255)

    def test_from_hsl_grayscale(self):
        """Test HSL with 0 saturation produces gray."""
        color = Color.from_hsl(0, 0, 0.5)
        r, g, b = color.to_rgb()
        assert r == g == b

    def test_from_hsl_hue_out_of_range_high(self):
        """Test error on hue > 360."""
        with pytest.raises(ColorError):
            Color.from_hsl(361, 0.5, 0.5)

    def test_from_hsl_hue_negative(self):
        """Test error on negative hue."""
        with pytest.raises(ColorError):
            Color.from_hsl(-1, 0.5, 0.5)

    def test_from_hsl_saturation_out_of_range(self):
        """Test error on saturation > 1."""
        with pytest.raises(ColorError):
            Color.from_hsl(120, 1.1, 0.5)

    def test_from_hsl_lightness_out_of_range(self):
        """Test error on lightness > 1."""
        with pytest.raises(ColorError):
            Color.from_hsl(120, 0.5, 1.1)


class TestColorConversions:
    """Test color format conversions."""

    def test_hex_to_rgb_roundtrip(self):
        """Test hex -> RGB conversion accuracy."""
        original_hex = "#FF5733"
        color = Color.from_hex(original_hex)
        assert color.to_hex() == original_hex

    def test_rgb_to_hex_roundtrip(self):
        """Test RGB -> hex conversion accuracy."""
        rgb = (255, 87, 51)
        color = Color.from_rgb(*rgb)
        converted = color.to_hex()
        color2 = Color.from_hex(converted)
        assert color2.to_rgb() == rgb

    def test_hsl_to_rgb_roundtrip(self):
        """Test HSL -> RGB -> HSL roundtrip within tolerance."""
        color = Color.from_hsl(180, 0.75, 0.5)
        h, s, l = color.to_hsl()
        # Allow 1% tolerance due to rounding
        assert abs(h - 180) < 2
        assert abs(s - 0.75) < 0.02
        assert abs(l - 0.5) < 0.02

    def test_to_hex_uppercase(self):
        """Test hex output is uppercase."""
        color = Color.from_rgb(255, 87, 51)
        hex_out = color.to_hex()
        assert hex_out.isupper()
        assert hex_out.startswith("#")

    def test_to_rgb_returns_tuple(self):
        """Test RGB output is a tuple."""
        color = Color.from_hex("#FF5733")
        rgb = color.to_rgb()
        assert isinstance(rgb, tuple)
        assert len(rgb) == 3

    def test_to_hsl_returns_tuple(self):
        """Test HSL output is a tuple."""
        color = Color.from_hex("#FF5733")
        hsl = color.to_hsl()
        assert isinstance(hsl, tuple)
        assert len(hsl) == 3

    def test_complex_roundtrip_hex_to_hsl_to_hex(self):
        """Test hex -> HSL -> hex roundtrip."""
        original = "#FF5733"
        color = Color.from_hex(original)
        h, s, l = color.to_hsl()
        color2 = Color.from_hsl(h, s, l)
        # Should convert back to similar hex (within rounding)
        rgb1 = Color.from_hex(original).to_rgb()
        rgb2 = color2.to_rgb()
        assert all(abs(a - b) <= 1 for a, b in zip(rgb1, rgb2))


class TestColorManipulation:
    """Test color manipulation methods."""

    def test_lighten_increases_lightness(self):
        """Test lighten method increases lightness."""
        original = Color.from_hsl(120, 0.5, 0.5)
        lightened = original.lighten(0.1)
        _, _, l_orig = original.to_hsl()
        _, _, l_light = lightened.to_hsl()
        assert l_light > l_orig

    def test_darken_decreases_lightness(self):
        """Test darken method decreases lightness."""
        original = Color.from_hsl(120, 0.5, 0.5)
        darkened = original.darken(0.1)
        _, _, l_orig = original.to_hsl()
        _, _, l_dark = darkened.to_hsl()
        assert l_dark < l_orig

    def test_saturate_increases_saturation(self):
        """Test saturate method increases saturation."""
        original = Color.from_hsl(120, 0.3, 0.5)
        saturated = original.saturate(0.2)
        _, s_orig, _ = original.to_hsl()
        _, s_sat, _ = saturated.to_hsl()
        assert s_sat > s_orig

    def test_desaturate_decreases_saturation(self):
        """Test desaturate method decreases saturation."""
        original = Color.from_hsl(120, 0.8, 0.5)
        desaturated = original.desaturate(0.2)
        _, s_orig, _ = original.to_hsl()
        _, s_desat, _ = desaturated.to_hsl()
        assert s_desat < s_orig

    def test_lighten_clamps_at_max(self):
        """Test lighten clamps at lightness=1."""
        color = Color.from_hsl(120, 0.5, 0.9)
        lightened = color.lighten(0.2)  # Would exceed 1.0
        _, _, l = lightened.to_hsl()
        assert l <= 1.0

    def test_darken_clamps_at_min(self):
        """Test darken clamps at lightness=0."""
        color = Color.from_hsl(120, 0.5, 0.1)
        darkened = color.darken(0.2)  # Would go below 0.0
        _, _, l = darkened.to_hsl()
        assert l >= 0.0

    def test_complement_hue_offset(self):
        """Test complement method rotates hue by 180 degrees."""
        color = Color.from_hsl(30, 0.5, 0.5)
        complemented = color.complement()
        h_orig, _, _ = color.to_hsl()
        h_comp, _, _ = complemented.to_hsl()
        expected_hue = (h_orig + 180) % 360
        assert abs(h_comp - expected_hue) < 1

    def test_mix_equal_weight_produces_intermediate(self):
        """Test mix with weight=0.5 produces intermediate color."""
        color1 = Color.from_rgb(255, 0, 0)  # Red
        color2 = Color.from_rgb(0, 0, 255)  # Blue
        mixed = color1.mix(color2, 0.5)
        r, g, b = mixed.to_rgb()
        assert 100 < r < 180  # Between pure red and mixed
        assert 0 <= g <= 20   # Minimal green
        assert 100 < b < 180  # Between pure blue and mixed

    def test_mix_weight_zero(self):
        """Test mix with weight=0 returns first color."""
        color1 = Color.from_rgb(255, 0, 0)
        color2 = Color.from_rgb(0, 0, 255)
        mixed = color1.mix(color2, 0)
        assert mixed.to_rgb() == color1.to_rgb()

    def test_mix_weight_one(self):
        """Test mix with weight=1 returns second color."""
        color1 = Color.from_rgb(255, 0, 0)
        color2 = Color.from_rgb(0, 0, 255)
        mixed = color1.mix(color2, 1.0)
        assert mixed.to_rgb() == color2.to_rgb()

    def test_mix_invalid_weight_negative(self):
        """Test mix with negative weight raises error."""
        color1 = Color.from_rgb(255, 0, 0)
        color2 = Color.from_rgb(0, 0, 255)
        with pytest.raises(ColorError):
            color1.mix(color2, -0.1)

    def test_mix_invalid_weight_exceeds_one(self):
        """Test mix with weight > 1 raises error."""
        color1 = Color.from_rgb(255, 0, 0)
        color2 = Color.from_rgb(0, 0, 255)
        with pytest.raises(ColorError):
            color1.mix(color2, 1.1)


class TestColorImmutability:
    """Test that Color objects are immutable."""

    def test_manipulation_returns_new_instance(self):
        """Test that manipulation methods return new instances."""
        original = Color.from_hex("#FF5733")
        lightened = original.lighten(0.1)
        assert original is not lightened
        assert original.to_hex() == "#FF5733"


class TestColorSpecialCases:
    """Test edge cases and special scenarios."""

    def test_pure_red(self):
        """Test pure red color conversions."""
        color = Color.from_hex("#FF0000")
        assert color.to_rgb() == (255, 0, 0)
        h, s, l = color.to_hsl()
        assert abs(h - 0) < 1  # Hue should be ~0 for red

    def test_pure_green(self):
        """Test pure green color conversions."""
        color = Color.from_hex("#00FF00")
        assert color.to_rgb() == (0, 255, 0)
        h, s, l = color.to_hsl()
        assert abs(h - 120) < 1  # Hue should be ~120 for green

    def test_pure_blue(self):
        """Test pure blue color conversions."""
        color = Color.from_hex("#0000FF")
        assert color.to_rgb() == (0, 0, 255)
        h, s, l = color.to_hsl()
        assert abs(h - 240) < 1  # Hue should be ~240 for blue

    def test_gray_has_zero_saturation(self):
        """Test that gray colors have 0 saturation."""
        color = Color.from_rgb(128, 128, 128)
        _, s, _ = color.to_hsl()
        assert s < 0.01  # Effectively zero

    def test_repr_includes_hex(self):
        """Test Color repr includes hex value."""
        color = Color.from_hex("#FF5733")
        repr_str = repr(color)
        assert "FF5733" in repr_str or "ff5733" in repr_str

    def test_chain_manipulations(self):
        """Test chaining multiple manipulations."""
        color = Color.from_hex("#FF5733")
        result = color.lighten(0.1).saturate(0.2).complement()
        # Should not raise error and return a Color
        assert isinstance(result, Color)
