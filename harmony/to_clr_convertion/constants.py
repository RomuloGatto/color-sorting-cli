import typer


class CLRSpecialBytes:
    """Store the special chunks of bytes of the MacOS CLR file format"""

    CLASS_DECLARATION_BYTES: bytes = b"\x84\x84\x84"
    COLOR_COUNT_CHUNK_START: bytes = b"\x84\x02\x40\x69\x85"
    COLOR_DESCRIPTION_START: bytes = b"\x84\x96\x9a"
    COLOR_ITEM_START: bytes = b"\x94\x84\x93\x97\x01\x98"
    COLORS_COMPONENTS_CHUNK_START: bytes = (
        b"\x85\x84\x01\x63\x01\x84\x04\x66\x66\x66\x66"
    )
    COLORS_NAMES_CHUNK_START: bytes = b"\x01\x94\x84\x01\x2b"
    END_OF_DATA_BYTE: bytes = b"\x86"
    FLOAT_BYTE: bytes = b"\x83"
    INHERITANCE_DECLARATION_BYTES: bytes = b"\x84\x84"
    INTEGER_16_BYTE: bytes = b"\x81"
    MAXIMUM_COMPONENT_VALUE: bytes = b"\x01"
    MINIMUM_COMPONENT_VALUE: bytes = b"\x00"
    NEW_COLOR_MAP: bytes = b"\x84\x02\x40\x40"
    NSOBJECT_CLASS_NAME_COUNT: bytes = b"\x08"
    NSOBJECT_CLASS_NAME: bytes = b"NSObject"
    NSSTRING_TYPE_NAME: bytes = b"NSString"
    NULL_BYTE: bytes = b"\x00"
    SIGNATURE: bytes = b"\x04\x0bstreamtyped"
    START_OF_FILE: bytes = b"\x81\xe8\x03\x84\x01\x69\x01"

    @classmethod
    def get_file_start(cls) -> bytearray:
        """Return the initial bytes of the CLR file format"""
        file_start = bytearray(cls.SIGNATURE)
        file_start.extend(cls.START_OF_FILE)

        return file_start


class TXT2CLRCommandArguments:
    """Store the "txt2clr" command arguments"""

    colors_file: typer.FileText = typer.Argument(..., help="File to be converted")
