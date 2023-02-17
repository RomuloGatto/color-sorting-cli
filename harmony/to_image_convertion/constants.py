# pylint: disable=too-few-public-methods
from pathlib import Path

from harmony import core


class TXT2ImageCommandArguments:
    """Store the "txt2clr" command arguments"""

    file_path: Path = core.make_file_path_argument(
        "File with the colors to be represented"
    )
