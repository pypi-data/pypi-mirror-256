"""
A library to allow developers to ensure that any strings can be translated.

This library ensures that all strings passed to other libraries/services
can be stored and translated later based on locale.
"""
import sys
from types import ModuleType
from typing import Dict, Optional

from dd_lib_i18n_base import logger
from dd_lib_i18n_base.exceptions import (
    MissingMessagesFileException,
    ModuleNotFoundException,
    UnreadableMessagesFileException,
)
from dd_lib_i18n_base.internal import Param, get_messages, handle_missing_message_error
from dd_lib_i18n_base.message import InternationalisedException, Message


class I18n:
    """
    A namespaced instance to retrieve messages and errors from.

    NOTE: Will error if `messages.properties` file is missing.

    @param namespace: The module to namespace the i18n to.
                      Must be a sibling to a `messages.properties` file.
    """

    def __init__(self, namespace: ModuleType):
        try:
            messages = get_messages(namespace)
        except MissingMessagesFileException as mmfe:
            logger.exception(mmfe)
            raise
        except UnreadableMessagesFileException as umfe:
            logger.exception(umfe)
            raise

        self._namespace = namespace
        self._messages: Dict[str, str] = messages

    def message(self, key: str, params: Optional[Dict[str, Param]] = None) -> Message:
        """
        Create a `Message` within this namespace.

        NOTE: Will not error if message key is missing.

        @param key: the key to look up in the messages file.
        @param params: (Optional) the named parameters (if any) needed to format the message.
        """
        message = self._messages.get(key, None)

        if message is None:
            handle_missing_message_error(self._namespace.__name__, key)

        return Message(
            namespace=self._namespace.__name__, key=key, params=params, message=message
        )

    def error(
        self,
        key: str,
        params: Optional[Dict[str, Param]] = None,
    ) -> InternationalisedException:
        """
        Create an `InternationalisedException` within this namespace.

        NOTE: Will not error if message key is missing.

        @param key: the key to look up in the messages file.
        @param params: (Optional) the named parameters (if any) needed to format the message.
        """
        return InternationalisedException(self.message(key, params))


class CustomInternationalisedException(InternationalisedException):
    """
    A handily subclassable exception that can be translated later.

    Subclasses should specify the following class variables:
        key = The default message key string
        i18n = The I18n instance with the relevent messages
    """

    # Subclasses should override these class variables
    key: str = ""
    i18n: Optional[I18n] = None

    @classmethod
    def create(
        cls, params: Optional[Dict[str, Param]] = None, key: Optional[str] = None
    ) -> InternationalisedException:
        """
        Create a serialisable instance of a custom internationalised exception.

        If passed, the `key` parameter will override the default key for this exception.

        @raises AttributeError is the class cannot be used to create a message.
        """
        key = key or cls.key

        if key == "":
            raise AttributeError(f"No key for error {str(cls)}")

        if cls.i18n is None:
            raise AttributeError(f"No i18n for error {str(cls)}")

        return cls(cls.i18n.message(key, params))


def get_i18n(module_name: str) -> I18n:
    """
    Get an I18n instance from a module name.

    @raises ModuleNotFoundException if the module name given does not resolve to a module
    """
    try:
        module = sys.modules[module_name]
        return I18n(module)
    except KeyError as key_error:
        raise ModuleNotFoundException(module_name) from key_error
