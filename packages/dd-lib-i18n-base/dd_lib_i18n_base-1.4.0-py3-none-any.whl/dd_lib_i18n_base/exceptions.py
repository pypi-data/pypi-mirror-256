"""All the exceptions raised by I18n-base library"""


class I18nException(Exception):
    """Base exception for all exceptions thrown by I18n-base library"""

    def __init__(self, message: str, namespace: str):
        super().__init__(message)
        self.message = message
        self.namespace = namespace

    def __reduce__(self):
        return (I18nException, (self.message, self.namespace))


class ModuleNotFoundException(I18nException):
    """Raised when the module name given cannot be resolved to a module"""

    def __init__(self, namespace: str):
        super().__init__(f"Cannot find module '{namespace}'", namespace=namespace)

    def __reduce__(self):  # pyright: ignore [reportIncompatibleMethodOverride]
        return (ModuleNotFoundException, (self.namespace,))


class MissingMessagesFileException(I18nException):
    """Raised when the messages file is missing"""

    def __init__(self, namespace: str):
        super().__init__(
            f"Missing `messages.properties` file for {namespace}", namespace=namespace
        )

    def __reduce__(self):  # pyright: ignore [reportIncompatibleMethodOverride]
        return (MissingMessagesFileException, (self.namespace,))


class UnreadableMessagesFileException(I18nException):
    """Raised when there is an error reading the messages file"""

    def __init__(self, namespace: str):
        super().__init__(
            f"Unreadable `messages.properties` file for {namespace}", namespace=namespace
        )

    def __reduce__(self):  # pyright: ignore [reportIncompatibleMethodOverride]
        return (UnreadableMessagesFileException, (self.namespace,))
