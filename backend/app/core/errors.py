class StatForgeError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ExternalServiceError(StatForgeError):
    def __init__(self, message: str, provider: str, status_code: int = 502) -> None:
        super().__init__(message=message, status_code=status_code)
        self.provider = provider


class ConfigurationError(StatForgeError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=500)


class ResourceNotFoundError(StatForgeError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=404)
