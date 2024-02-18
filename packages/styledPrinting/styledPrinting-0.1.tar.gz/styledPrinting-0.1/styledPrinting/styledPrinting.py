from contants import COLORS, BACKGROUNDS, STYLES, CURSOR

def checkType(value: str, type_: str, optional: bool = False) -> None:
	"""Check if the value is of the specified type

	Args:
			value (str): The value to be checked
			type_ (str): The type to be checked
			optional (bool, optional): If the value can be None. Defaults to False.
	"""
	if not isinstance(value, type_) and not (optional and value is None):
		raise TypeError(f"Expected {type_} but got {type(value)}")


def cursorMove(operation: CURSOR) -> None:
	"""Move the cursor

	Args:
			operation (CURSOR): The operation to be performed
	"""
	if not isinstance(operation, CURSOR):
		raise TypeError(f"Expected {CURSOR} but got {type(operation)}")
	print(operation.value, end="")


def eraseLine() -> None:
	"""Erase the current line"""
	print(CURSOR.LINE_START.value + "\033[K", end="")


def styleText(
	text: str,
	color: COLORS | None = None,
	background: BACKGROUNDS | None = None,
	style: STYLES | None = None,
) -> None:
	"""Style a text

	Args:
			text (str): The text to be styled
			color (COLORS | None, optional): The color of the text. Defaults to None.
			background (BACKGROUNDS | None, optional): The background color of the text. Defaults to None.
			style (STYLES | None, optional): The style of the text. Defaults to None.

	Returns:
			str: The styled text
	"""
	if not isinstance(text, str):
		raise TypeError(f"Expected {str} but got {type(text)}")
	elif not isinstance(color, COLORS) and color is not None:
		raise TypeError(f"Expected {COLORS} but got {type(color)}")
	elif not isinstance(background, BACKGROUNDS) and background is not None:
		raise TypeError(f"Expected {BACKGROUNDS} but got {type(background)}")
	elif not isinstance(style, STYLES) and style is not None:
		raise TypeError(f"Expected {STYLES} but got {type(style)}")
	return (
		(f"{color.value}" if color else "")
		+ (f"{background.value}" if background else "")
		+ (f"{style.value}" if style else "")
		+ text
		+ (f"{COLORS.ENDC.value}" if color else "")
		+ (f"{BACKGROUNDS.ENDC.value}" if background else "")
		+ (f"{STYLES.ENDC.value}" if style else "")
	)

styleText("Hello, World!", color=COLORS.RED, background=BACKGROUNDS.CYAN, style=STYLES.BOLD)