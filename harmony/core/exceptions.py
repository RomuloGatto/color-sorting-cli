class InvalidFileException(Exception):
    """Raised when a invalid path is passed"""


class InvalidColorException(Exception):
    """Raised when a color is inputted as an invalid format"""


class InvalidObjectToSaveException(Exception):
    """Raised when an invalid object is passed to be saved in the database"""


class NoExtensionFoundException(Exception):
    """Raised during attempt to extract the extension of a file from a file name or path
    the has no externsion"""


class NoColorsFoundException(Exception):
    """Raised when no color was extracted during the reading"""


class InvalidColorFormatException(Exception):
    """Raised when the color format passed was not the expected"""


class InvalidRegexException(Exception):
    """Raised when a regex does not match when it should"""
