"""
This file contains utility functions that are used across the application.
"""

import logging
import re
from pathlib import Path

logging.basicConfig(level=logging.ERROR)


def get_project_root() -> str:
    """
    Returns the root path of the project.
    """
    return str(Path(__file__).parent.parent)


def get_links_from_text(text: str) -> list[str]:
    """
    Returns a list of links found in the given text.
    """
    link_regex = \
        r'((http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))'
    matches = re.findall(link_regex, text)
    return [match[0] for match in matches]
