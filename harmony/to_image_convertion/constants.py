from pathlib import Path

from harmony.core.constants import make_file_path_argument


class TXT2ImageCommandArguments:
    """Store the "txt2clr" command arguments"""

    file_path: Path = make_file_path_argument("File with the colors to be represented")
