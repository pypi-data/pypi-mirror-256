"""A module containing things that can be translated later."""
from typing import Dict, Optional

from dd_lib_i18n_base import logger
from dd_lib_i18n_base.internal import Param


class Message:
    """A namespaced, parameterised message that can be translated later, if needed."""

    def __init__(
        self,
        namespace: str,
        key: str,
        params: Optional[Dict[str, Param]],
        message: Optional[str],
    ):
        self.namespace = namespace
        self.key = key
        self.params = params if params is not None else {}
        self._message = message

    def to_string(self) -> str:
        """Formats the message with the given parameters, to make it human readable."""
        if self._message is None:
            # fall back to using "readable" key and providing params dict
            message = f'{self.namespace.replace(".", " ")} - {self.key.replace(".", " ")}'
            params = "" if len(self.params) == 0 else f": {str(self.params)}"
            return message + params

        params_to_use = dict(self.params)

        while True:
            try:
                return self._message.format(**params_to_use)
            except KeyError as key_error:
                missing_param = str(key_error).replace("'", "")
                logger.error(
                    "Missing parameter {missing_param} for message {key} in {namespace}",
                    missing_param=missing_param,
                    key=self.key,
                    namespace=self.namespace,
                )
                params_to_use[
                    missing_param
                ] = f"[MISSING {missing_param}]"  # This is not internationalised

    def __reduce__(self):
        return (Message, (self.namespace, self.key, self.params, self._message))


class InternationalisedException(Exception):
    """An exception that can be translated later."""

    def __init__(self, message: Message):
        self.message = message
        super().__init__(self.message.to_string())

    def __repr__(self):
        return self.message.to_string()

    def __reduce__(self):
        return (self.__class__, (self.message,))
