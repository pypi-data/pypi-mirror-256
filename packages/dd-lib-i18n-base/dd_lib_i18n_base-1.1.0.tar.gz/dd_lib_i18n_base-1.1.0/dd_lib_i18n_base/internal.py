"""Module with helpful INTERNAL things for I18n-base library."""
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Dict, Optional, Union

from dd_lib_i18n_base import logger
from dd_lib_i18n_base.exceptions import (
    MissingMessagesFileException,
    UnreadableMessagesFileException,
)

Param = Union[str, int, float]


@dataclass
class _ParsedLine:
    key: str
    message: str


def get_messages(namespace: ModuleType) -> Dict[str, str]:
    """
    Get and parse the messages file for a namespace

    @raises MissingMessagesFileException if messages file is missing
    @raises UnreadableMessagesFileException if any other error occurs during parsing
    """
    if namespace.__file__ is None:
        raise UnreadableMessagesFileException(namespace.__name__)

    path = Path(namespace.__file__).parent / "messages.properties"

    if not path.exists() or not path.is_file():
        raise MissingMessagesFileException(namespace.__name__)

    messages = {}

    try:
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file:
                parsed_line = _parse_message_line(line)

                if parsed_line is not None:
                    messages[parsed_line.key] = parsed_line.message
    except OSError as ose:
        # Can this ever happen?
        raise UnreadableMessagesFileException(namespace.__name__) from ose

    return messages


def handle_missing_message_error(namespace: str, key: str) -> None:
    """Handy patchable method for handling missing message errors."""
    logger.error(f"No message was found for key '{key}' in {namespace}")


def _parse_message_line(line: str) -> Optional[_ParsedLine]:
    line = line.rstrip()  # removes trailing whitespace and '\n' chars

    if "=" not in line:
        return None  # skips blanks and comments w/o =
    if line.startswith("#"):
        return None  # skips comments which contain =

    key, message = line.split("=", 1)
    return _ParsedLine(key=key.strip(), message=message.strip())
