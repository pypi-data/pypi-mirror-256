class Effect:
    """Class to represent the effects of the text

        Usage:
        ```python
        red = Effect("\033[91m")

        print(red("Hello, World!"))
        print(f"{red}Hello, World!\033[0m")
    ```
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        """Returns the value of the effect

        Returns:
            str: The value of the effect
        """
        return self.value

    def __repr__(self) -> str:
        """Returns the value of the effect

        Returns:
            str: The value of the effect
        """
        return self.value

    def __call__(self, text: str) -> str:
        """Returns the text with the effect applied

        Args:
            text (str): The text to apply the effect

        Returns:
            str: The text with the effect applied
        """
        return f"{self.value}{text}\033[0m"


class Color:
    """Class to represent the colors of the text

    Usage:
    ```python
    print(Color.red("Hello, World!"))
    print(f"{Color.red}Hello, World!{Color.reset}")
    ```
    """

    red: Effect = Effect("\033[91m")
    green: Effect = Effect("\033[92m")
    yellow: Effect = Effect("\033[93m")
    blue: Effect = Effect("\033[94m")
    purple: Effect = Effect("\033[95m")
    cyan: Effect = Effect("\033[96m")
    white: Effect = Effect("\033[97m")
    reset: Effect = Effect("\033[0m")


class Background:
    """Class to represent the background colors of the text

    Usage:
    ```python
    print(Background.red("Hello, World!"))
    print(f"{Background.red}Hello, World!{Background.reset}")
    ```
    """

    red: Effect = Effect("\033[41m")
    green: Effect = Effect("\033[42m")
    yellow: Effect = Effect("\033[43m")
    blue: Effect = Effect("\033[44m")
    purple: Effect = Effect("\033[45m")
    cyan: Effect = Effect("\033[46m")
    white: Effect = Effect("\033[47m")
    reset: Effect = Effect("\033[0m")


class Style:
    """Class to represent the styles of the text

    Usage:
    ```python
    print(Style.bold("Hello, World!"))
    print(f"{Style.bold}Hello, World!{Style.reset}")
    ```
    """

    bold: Effect = Effect("\033[1m")
    underline: Effect = Effect("\033[4m")
    blink: Effect = Effect("\033[5m")
    inverted: Effect = Effect("\033[7m")
    concealed: Effect = Effect("\033[8m")
    strike: Effect = Effect("\033[9m")
    reset: Effect = Effect("\033[0m")


class CursorBase:
    """Class to represent the cursor movement

    Usage:
    ```python
    cursorUp = CursorBase("\033[A")

    print(cursorUp, end="") # Move the cursor up 1 line
    print(cursorUp(3), end="") # Move the cursor up 3 lines
    ```
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        """Returns the value of the cursor

        Returns:
            str: The value of the cursor
        """
        return self.value

    def __repr__(self) -> str:
        """Returns the value of the cursor

        Returns:
            str: The value of the cursor
        """
        return self.value

    def __call__(self, times: int = 1) -> None:
        '''Prints the cursor movement command to the console, X times.

        This method does not return a value. Instead, it directly prints the ANSI escape codes 
        for the cursor movement to the console. The actual movement of the cursor will not 
        occur until the output is flushed (for example, by printing a newline or manually 
        flushing the output).

        Args:
            times (int, optional): The number of times to print the cursor movement command. Defaults to 1.
        '''
        print(f"{self.value * times}", end="")


class Cursor:
    """Class to represent the cursor movement

    Usage:
    ```python
    Cursor.moveUp() # Move the cursor up 1 line

    Cursor.moveUp(3) # Move the cursor up 3 lines

    print(f"{Cursor.moveUp}Hello, World!") # Move the cursor up 1 line and print "Hello, World!"
    ```
    """

    moveUp: CursorBase = CursorBase("\033[A")
    moveDown: CursorBase = CursorBase("\033[B")
    moveLineStart: CursorBase = CursorBase("\033[1G")
    moveLineEnd: CursorBase = CursorBase("\033[K")
    moveLeft: CursorBase = CursorBase("\033[D")
    moveRight: CursorBase = CursorBase("\033[C")
    clearLine: CursorBase = CursorBase("\033[2K")
    clearScreen: CursorBase = CursorBase("\033[2J")
    saveCursorPosition: CursorBase = CursorBase("\033[s")
    restoreCursorPosition: CursorBase = CursorBase("\033[u")
    hideCursor: CursorBase = CursorBase("\033[?25l")
    showCursor: CursorBase = CursorBase("\033[?25h")

    @staticmethod
    def move(x: int = 0, y: int = 0, relative: bool = False) -> None:
        """Moves the cursor to the position x, y

        Args:
            x (int, optional): The x position. Defaults to 0.
            y (int, optional): The y position. Defaults to 0.
            relative (bool, optional): If the position is relative to the current position. Defaults to False.

        Usage:
        ```python
        Cursor.move(3, 4) # Move the cursor to the position 3, 4

        Cursor.move(3, 4, relative=True) # Move the cursor 3 to the right and 4 down, so the cursor will be at 6, 8; Given that the cursor is at 3, 4
        ```
        """
        if relative:
            if x > 0:
                print(f"\033[{x}C", end="")
            elif x < 0:
                print(f"\033[{abs(x)}D", end="")
            if y > 0:
                print(f"\033[{y}B", end="")
            elif y < 0:
                print(f"\033[{abs(y)}A", end="")
        else:
            print(f"\033[{y};{x}H", end="")
