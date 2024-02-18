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

class CURSOR(Enum):
    LINE_UP: str = "\033[A"
    LINE_DOWN: str = "\033[B"
    LINE_START: str = "\033[1G"
    LINE_END: str = "\033[K"
    CHAR_BACK: str = "\033[D"
    CHAR_FORWARD: str = "\033[C"

