# Styled Printing

## Description
This is a simple module to help you print styled text to the console and to operate with the console cursor.

## Installation
```bash
pip install styledPrinting
```

## Usage

```python
from styledPrinting import Color

print(Color.red("This is red text"))
print(f"{Color.red}This is red text{Color.reset}")
```

```python
from styledPrinting import Background

print(Background.red("This is red background"))
print(f"{Background.red}This is red background{Background.reset}")
```

```python
from styledPrinting import Style

print(Style.bold("This is bold text"))
print(f"{Style.bold}This is bold text{Style.reset}")
```

```python
from styledPrinting import Cursor

Cursor.move(5, 5) # The cursor is now at the position (5, 5)

Cursor.move(3, 3) # The cursor is now at the position (3, 3)

Cursor.move(3, 3, relative=True) # The cursor is now at the position (6, 6); Given that the previous position was (3, 3)
```

```python
from styledPrinting import Cursor

Cursor.moveUp() # Move the cursor up 1 line

Cursor.moveUp(3) # Move the cursor up 3 lines

print(f"{Cursor.moveUp}Hello, World!") # Move the cursor up 1 line and print "Hello, World!"
```