"""Terminal Styling and Color Formatting Module.

Provides custom prompt styling for InquirerPy, ANSI escape sequence constants,
and utility functions for printing, prompt styling, and colored terminal inputs.
"""

from typing import Any

from InquirerPy.utils import InquirerPyStyle

media_selection_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",  # Signature green for the main indicator
        "question": "#ffffff bold",  # Crisp white for main question text
        "pointer": "#45F705 bold",  # Sharp green cursor pointer
        "highlighted": "#45F705 bold",  # Active item lights up bright green
        "choice": "#d1d5db",  # Soft light grey for unselected options
        "selected": "#45F705 bold",  # Vibrant green confirmation state
        "answer": "#45F705 bold",  # Selected value display after submit
        "answered_question": "#9ca3af",  # Muted grey for completed prompt
        "instruction": "#FFB700 italic",  # Amber italic hint for navigation tips
        "long_instruction": "#6b7280",  # Muted secondary instructions (Ctrl+C hint)
    }
)

show_name_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "input": "#45F705 bold",  # Highlight user text entry in signature green
        "validator": "#ff6b6b bold",  # Crisp coral-red for empty input validation error
        "answered_question": "#9ca3af",
    }
)

show_selection_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "pointer": "#45F705 bold",
        "highlighted": "#45F705 bold",
        "choice": "#d1d5db",
        "instruction": "#38bdf8 italic",  # Sky blue for navigation instructions
        "answered_question": "#9ca3af",
    }
)

season_selection_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "pointer": "#38bdf8 bold",  # Sky-blue pointer to visually distinguish season select
        "highlighted": "#38bdf8 bold",
        "choice": "#d1d5db",
        "instruction": "#38bdf8 italic",
        "answered_question": "#9ca3af",
    }
)

checkpoint_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "pointer": "#45F705 bold",
        "highlighted": "#45F705 bold",
        "choice": "#d1d5db",
        "instruction": "#FFB700 italic",  # Amber hint text for next action guidance
        "answered_question": "#9ca3af",
    }
)

directory_selection_style = InquirerPyStyle(
    {
        "questionmark": "#10b981 bold",  # Emerald green for filesystem prompts
        "question": "#ffffff bold",
        "input": "#10b981 bold",  # Highlight active path entry in emerald green
        "pointer": "#10b981 bold",  # Folder completion autocomplete cursor
        "validator": "#ff6b6b bold",  # Path error warning color
        "answered_question": "#9ca3af",
    }
)

filetype_selection_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "pointer": "#45F705 bold",
        "highlighted": "#45F705 bold",
        "choice": "#d1d5db",
        "instruction": "#808080 italic",
        "answered_question": "#9ca3af",
    }
)

checkbox_selection_style = InquirerPyStyle(
    {
        "questionmark": "#06b6d4 bold",  # Cyan theme for batch selection state
        "question": "#ffffff bold",
        "pointer": "#06b6d4 bold",  # Cursor indicator
        "checkbox": "#06b6d4 bold",  # Unchecked [ ] visual key
        "enabled": "#45F705 bold",  # Checked [*] items in bright green
        "highlighted": "#06b6d4 bold",  # Active row under cursor
        "choice": "#9ca3af",
        "instruction": "#06b6d4 italic",  # Hints: [Space] Toggle, [Enter] Confirm
        "answered_question": "#9ca3af",
    }
)

confirmation_style = InquirerPyStyle(
    {
        "questionmark": "#facc15 bold",  # Vivid yellow for critical action confirmation
        "question": "#ffffff bold",
        "answer": "#45F705 bold",
        "answered_question": "#9ca3af",
        "instruction": "#facc15 italic",
    }
)

post_rename_style = InquirerPyStyle(
    {
        "questionmark": "#45F705 bold",
        "question": "#ffffff bold",
        "pointer": "#45F705 bold",
        "highlighted": "#45F705 bold",
        "choice": "#d1d5db",
        "instruction": "#FFB700 italic",
        "answered_question": "#9ca3af",
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
