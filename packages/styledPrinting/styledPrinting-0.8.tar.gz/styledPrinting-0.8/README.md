# Styled Printing

## Description
This is a simple module to help you print styled text to the console and to operate with the console cursor.

## Installation
```bash
pip install styledPrinting
```

## Usage

### Text Styling

```python
from styledPrinting import styleText, COLORS, BACKGROUNDS, STYLES

print(styleText("Hello, World!", COLORS.RED, BACKGROUNDS.CYAN, STYLES.BOLD))

print(styleText("Hello, World!", color=COLORS.BLUE))

print(styleText("Hello, World!", background=BACKGROUNDS.YELLOW))
```

### Cursor Operations

```python
from styledPrinting import cursorMove, eraseLine, CURSOR

print("Looping...")
for i in range(10):
	print(f"Line {i}")
	CURSOR.LINE_UP()
	eraseLine()
print("Done!")

print("Looping...")
for i in range(10):
	print(f"Line {i}")
	eraseLine(moveUpBefore=True)
print("Done!")
```