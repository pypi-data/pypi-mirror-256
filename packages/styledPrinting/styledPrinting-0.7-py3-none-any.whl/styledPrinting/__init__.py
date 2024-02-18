from enum import Enum


class COLORS(Enum):
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    BLUE: str = "\033[94m"
    PURPLE: str = "\033[95m"
    CYAN: str = "\033[96m"
    WHITE: str = "\033[97m"
    ENDC: str = "\033[0m"


class BACKGROUNDS(Enum):
    RED: str = "\033[41m"
    GREEN: str = "\033[42m"
    YELLOW: str = "\033[43m"
    BLUE: str = "\033[44m"
    PURPLE: str = "\033[45m"
    CYAN: str = "\033[46m"
    WHITE: str = "\033[47m"
    ENDC: str = "\033[0m"


class STYLES(Enum):
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    BLINK: str = "\033[5m"
    INVERTED: str = "\033[7m"
    CONCEALD: str = "\033[8m"
    STRIKE: str = "\033[9m"
    ENDC: str = "\033[0m"


class CursorOperation:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __call__(self, times: int = 1) -> str:
        print(self.value * times, end="")


class CURSOR:
    LINE_UP: CursorOperation = CursorOperation("\033[A")
    LINE_DOWN: CursorOperation = CursorOperation("\033[B")
    LINE_START: CursorOperation = CursorOperation("\033[1G")
    LINE_END: CursorOperation = CursorOperation("\033[K")
    CHAR_BACK: CursorOperation = CursorOperation("\033[D")
    CHAR_FORWARD: CursorOperation = CursorOperation("\033[C")


def checkType(value: str, type_: str, optional: bool = False) -> None:
    """Check if the value is of the specified type

    Args:
        value (str): The value to be checked
        type_ (str): The type to be checked
        optional (bool, optional): If the value can be None. Defaults to False.
    """
    if not isinstance(value, type_) and not (optional and value is None):
        raise TypeError(f"Expected {type_} but got {type(value)}")


def eraseLine(moveUpBefore: bool = False, moveUpAfter: bool = False) -> None:
    '''Clears the line where the cursor is

    Args:
        moveUpBefore (bool, optional): If the cursor should move up before clearing the line. Defaults to False.
        moveUpAfter (bool, optional): If the cursor should move up after clearing the line. Defaults to False.
    '''
    if moveUpBefore:
        CURSOR.LINE_UP()
    print("\033[1G\033[K", end="")
    if moveUpAfter:
        CURSOR.LINE_UP()


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
