"""
This file contains the TagNotFound exception, which is thrown when a Tag is not found
in a TEI XML file.
"""


class TagNotFoundInTeiXmlException(Exception):
    """
    The TagNotFoundInTeiXmlException is thrown when a Tag is not found in a TEI XML file.
    """

    def __init__(self, message: str | None = None) -> None:
        """
        Initializes the TagNotFoundInTeiXmlException object with an optional message.
        """
        self.message = message
        super().__init__(message)
