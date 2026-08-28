"""Terminal Styling and Color Formatting Module.

Provides custom prompt styling for InquirerPy, ANSI escape sequence constants,
and utility functions for printing, prompt styling, and colored terminal inputs.
"""

from typing import Any

from InquirerPy.utils import InquirerPyStyle

media_selection_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#21BCFF bold",
        "answered_question": "#9ca3af",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6b7280",
    }
)

show_title_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#21BCFF bold",
        "answered_question": "#9ca3af",
        "instruction": "#21BCFF italic",
        "long_instruction": "#7BF1A8 bold",
    }
)

show_selection_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#21BCFF bold",
        "answered_question": "#9CA3AF",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

post_manifest_action_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

directory_selection_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "input": "#FFB93B",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

filetype_selection_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#ffffff bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "input": "#FFB93B",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

confirm_prompt_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#FFB93B bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#21BCFF bold",
        "answer": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "input": "#FFB93B",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

post_rename_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#FFB93B bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#21BCFF bold",
        "choice": "#21BCFF bold",
        "selected": "#FFB93B bold",
        "mark": "#FFB93B bold",
        "answertag": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "checkbox": "#FFB93B",
        "checkbox_off": "#ffffff",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
    }
)

checkbox_selection_style = InquirerPyStyle(
    {
        "questionmark": "#FF692A bold",
        "question": "#FFB93B bold",
        "pointer": "#21BCFF bold",
        "highlighted": "#FFB93B bold",
        "choice": "#FFB93B bold",
        "selected": "#FFB93B bold",
        "enabled": "#FFB93B bold",
        "disabled": "#9CA3AF",
        "answertag": "#FFB93B bold",
        "answered_question": "#9CA3AF",
        "checkbox": "#FFB93B",
        "checkbox_off": "#ffffff",
        "instruction": "#21BCFF italic",
        "long_instruction": "#6B7280",
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

    # Regular colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BLUE = "\033[38;2;33;188;255m"
    YELLOW_1 = "\033[38;2;255;185;59m"
    MINT_GREEN = "\033[38;2;123;241;168m"

    # Bold colors
    RED_BOLD = "\033[1;31m"
    GREEN_BOLD = "\033[1;32m"
    YELLOW_BOLD = "\033[1;33m"
    BLUE_BOLD = "\033[1;34m"
    PURPLE_BOLD = "\033[1;35m"
    CYAN_BOLD = "\033[1;36m"
    WHITE_BOLD = "\033[1;37m"
    BLUE_BOLD = "\033[1;38;2;33;188;255m"
    YELLOW_BOLD_1 = "\033[1;38;2;255;185;59m"
    MINT_GREEN_BOLD = "\033[1;38;2;123;241;168m"

    # Underline
    RED_UNDERLINE = "\033[4;31m"
    GREEN_UNDERLINE = "\033[4;32m"
    YELLOW_UNDERLINE = "\033[4;33m"
    BLUE_UNDERLINE = "\033[4;34m"
    PURPLE_UNDERLINE = "\033[4;35m"
    CYAN_UNDERLINE = "\033[4;36m"
    WHITE_UNDERLINE = "\033[4;37m"
    BLUE_BOLD_UNDERLINE = "\033[4;38;2;33;188;255m"
    YELLOW_BOLD_UNDERLINE_1 = "\033[4;38;2;255;185;59m"
    MINT_GREEN_BOLD_UNDERLINE = "\033[4;38;2;123;241;168m"

    # Reset
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
    return sep.join(map(str, values)) + colors.RESET


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
    print(colors.RESET, end="")
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
