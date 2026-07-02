from typing import Any

from InquirerPy.utils import InquirerPyStyle

custom_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "input": "#ffffff",
        "pointer": "#45F705",
        "choice": "#ffffff",
        "selected": "#45F705",
        "separator": "#add8e6",
        "answer": "#45F705",  # The committed selection shown after choosing
        "answered_question": "#ffffff",  # The message text after the prompt is answered
        "validator": "#ff6b6b bold",  # Inline validation error text
        "highlighted": "#FF8800",  # The choice currently under the cursor
        "instruction": "#808080",  # Secondary hint text e.g. "(Use arrow keys)"
        "long_instruction": "#808080",  # Secondary hint text e.g. "(Use arrow keys)"
    }
)


class colors:  # noqa: N801
    """A collection of ANSI escape codes for terminal text formatting and coloring.

    Attributes:
        GREEN (str): ANSI code for bright green text.
        ERROR (str): ANSI code for bright yellow text (commonly used for warnings).
        BLUE (str): ANSI code for blue text.
        YELLOW (str): ANSI code for yellow text.
        MAGENTA (str): ANSI code for magenta text.
        CYAN (str): ANSI code for cyan text.
        RED (str): ANSI code for red text.
        END (str): ANSI code to reset formatting back to default.
        BOLD (str): ANSI code to make text bold.
        UNDERLINE (str): ANSI code to underline text.
        RESET (str): ANSI code to reset formatting back to default.
    """

    WHITE = "\033[37m"
    GREEN = "\033[92m"
    ERROR = "\033[93m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    GREY = "\033[90m"
    END = "\x1b[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def color(*values: Any, sep: str = "") -> str:
    """Decorates and combines strings with ANSI styling codes, ensuring safe closure.

    This function automatically appends the `colors.END` code to the end of the
    generated string. This prevents formatting or color leaking into subsequent
    terminal output.

    Args:
        *values (Any): Positional arguments consisting of style codes and text strings
            interspersed (e.g., color, text, color, text).
        sep (str, optional): The string used to join the values together. Defaults to "".

    Returns:
        str: A single joined string wrapped with the provided ANSI styles and a trailing reset code.

    Example:
        >>> color(colors.GREEN, "Success", colors.BOLD, " Fully Loaded")
        '\x033[92mSuccess\033[1m Fully Loaded\x1b[0m'
    """
    return sep.join(map(str, values)) + colors.END


def cinput(*prompt: Any, input_color: str = "") -> str:
    """Prompts the user for input using formatted, colored text.

    It allows styling the question prompt itself, and optionally styles the text
    the user types into the terminal. It safely resets terminal colors after the
    input is submitted.

    Args:
        *prompt (Any): The components of the prompt message, matching the positional
            argument format used in `color()`.
        input_color (str, optional): An ANSI escape code to color the text typed
            by the user. Defaults to "".

    Returns:
        str: The string entered by the user.

    Example:
        >>> user_name = cinput(
        ...     colors.CYAN, "Enter your name: ", input_color=colors.GREEN
        ... )
    """
    inp = input(color(*prompt) + input_color)
    print(colors.END, end="")
    return inp


def cprint(*values: Any, sep: str = "", **kwargs: Any) -> None:
    """Prints styled and colored text directly to the console.

    A drop-in wrapper around Python's built-in `print()` that automatically formats
    the inputs using ANSI color escapes and appends a color reset code to prevent leaks.

    Args:
        *values (Any): Positional arguments of styles and text to be printed.
        sep (str, optional): The string used to separate multiple values. Defaults to "".
        **kwargs (Any): Arbitrary keyword arguments passed directly to the built-in
            `print()` function (e.g., `end`, `file`, `flush`).

    Example:
        >>> cprint(colors.RED, "An error occurred!", file=sys.stderr)
    """
    print(color(*values, sep=sep), **kwargs)
