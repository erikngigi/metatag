"""Application Theme and Color Definitions.

Centralizes UI style configurations for InquirerPy menus and provides a
structured namespace class for ANSI raw terminal formatting.
"""

from InquirerPy.utils import InquirerPyStyle

# Keep the InquirerPyStyle object as is since it expects a specific directory structure
custom_style = InquirerPyStyle(
    {
        "questionmark": "#ff9e3b bold",  # Orange '?' mark
        "question": "#ffffff bold",  # White bold prompt text
        "input": "#00ffcc",  # Cyan user input text
        "pointer": "#00ffcc bold",  # Selection cursor arrow
        "choice": "#ffffff",
    }
)


class Theme:
    """Namespace container for raw terminal ANSI color sequences."""

    # Text Styles
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"

    # Foreground Colors
    RED = "\033[91m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    GREY = "\033[90m"
