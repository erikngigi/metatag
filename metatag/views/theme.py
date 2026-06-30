"""Application Theme and Color Definitions.

Centralizes UI style configurations for InquirerPy menus and provides a
structured namespace class for ANSI raw terminal formatting.
"""

from InquirerPy.utils import InquirerPyStyle

custom_style = InquirerPyStyle(
    {
        "questionmark": "#00bbff bold",
        "question": "#00bbff bold",
        "input": "#ffffff",
        "pointer": "#00bbff",
        "choice": "#ffffff",
        "selected": "#00bbff",
        "separator": "#add8e6",
        "answer": "#00bbff",  # The committed selection shown after choosing
        "answered_question": "#ffffff",  # The message text after the prompt is answered
        "validator": "#ff6b6b bold",  # Inline validation error text
        "highlighted": "#FF8800",  # The choice currently under the cursor
        "instruction": "#808080",  # Secondary hint text e.g. "(Use arrow keys)"
        "long_instruction": "#808080",  # Secondary hint text e.g. "(Use arrow keys)"
    }
)


class Theme:
    """Namespace container for raw terminal ANSI color sequences."""

    # Text Styles
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"

    # Foreground Colors
    BLUE = "\033[34m"
    RED = "\033[91m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    GREY = "\033[90m"
