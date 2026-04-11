# colortool

Convert and manipulate colors across HEX/RGB/HSL formats for developers.

## Installation

```bash
pip install colortool
```

## Usage

```python
from colortool import Color

# Create colors from different formats
color = Color.from_hex("#FF5733")
color = Color.from_rgb(255, 87, 51)
color = Color.from_hsl(9, 1.0, 0.6)

# Convert between formats
hex_str = color.to_hex()      # "#FF5733"
rgb_tuple = color.to_rgb()    # (255, 87, 51)
hsl_tuple = color.to_hsl()    # (9.0, 1.0, 0.6)

# Manipulate colors
lighter = color.lighten(0.1)
darker = color.darken(0.1)
saturated = color.saturate(0.2)
desaturated = color.desaturate(0.2)
complementary = color.complement()

# Mix colors
red = Color.from_hex("#FF0000")
blue = Color.from_hex("#0000FF")
purple = red.mix(blue, 0.5)

# Chain operations
result = color.lighten(0.1).saturate(0.2).complement()
```

## API Reference

### `Color` Class

#### Construction

- **`Color.from_hex(hex_string: str) -> Color`**
  - Parse hexadecimal color string
  - Accepts `"#RRGGBB"` or `"RRGGBB"` (6-char) or `"#RGB"` or `"RGB"` (3-char shorthand)
  - Case-insensitive
  - Example: `Color.from_hex("#FF5733")` or `Color.from_hex("F0A")`

- **`Color.from_rgb(red: int, green: int, blue: int) -> Color`**
  - Create from RGB values
  - Each component: 0-255
  - Example: `Color.from_rgb(255, 87, 51)`

- **`Color.from_hsl(hue: float, saturation: float, lightness: float) -> Color`**
  - Create from HSL values
  - Hue: 0-360 degrees
  - Saturation: 0-1
  - Lightness: 0-1
  - Example: `Color.from_hsl(9, 1.0, 0.6)`

#### Conversions

- **`to_hex() -> str`**
  - Convert to hexadecimal string format
  - Returns uppercase string with `#` prefix (e.g., `"#FF5733"`)

- **`to_rgb() -> tuple`**
  - Convert to RGB tuple
  - Returns `(red, green, blue)` with values 0-255

- **`to_hsl() -> tuple`**
  - Convert to HSL tuple
  - Returns `(hue, saturation, lightness)`
  - Hue: 0-360 degrees
  - Saturation and Lightness: 0-1

#### Manipulation

- **`lighten(amount: float) -> Color`**
  - Return lighter color by increasing lightness
  - Amount: 0-1
  - Returns new Color instance

- **`darken(amount: float) -> Color`**
  - Return darker color by decreasing lightness
  - Amount: 0-1
  - Returns new Color instance

- **`saturate(amount: float) -> Color`**
  - Return more saturated color
  - Amount: 0-1
  - Returns new Color instance

- **`desaturate(amount: float) -> Color`**
  - Return less saturated color
  - Amount: 0-1
  - Returns new Color instance

- **`complement() -> Color`**
  - Return complementary color (hue rotated 180 degrees)
  - Returns new Color instance

- **`mix(other: Color, weight: float) -> Color`**
  - Mix this color with another color
  - Weight: 0-1 (0 = this color, 1 = other color)
  - Returns new Color instance
  - Raises `ColorError` if weight is outside [0, 1]

### `ColorError` Exception

Exception raised for invalid color values or operations.

```python
try:
    color = Color.from_rgb(256, 100, 100)  # Out of range
except ColorError as e:
    print(f"Error: {e}")
```

## Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=src/colortool --cov-report=term-missing
```

## License

MIT License - Copyright 2026 Nripanka Das
