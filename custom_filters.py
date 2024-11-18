import re
import html
from markupsafe import Markup


def safe_br(text):
    """
    Escapes all HTML tags in the input text except for <br>.

    Args:
        text (str): The input string containing HTML.

    Returns:
        str: The escaped string with <br> tags preserved.
    """
    # Escape all HTML
    text = text.replace("\n", "<br>")
    escaped_text = html.escape(text)

    # Use regex to revert <br> tags back to their original form
    escaped_text = re.sub(r'&lt;br\s*/?&gt;', '<br>', escaped_text)

    return Markup(escaped_text)
