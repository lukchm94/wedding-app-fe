class AuthenticationError(Exception):
    """Exception raised for authentication errors."""

    pass


class ExpiredTokenError(Exception):
    """Exception raised for expired tokens."""

    pass


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User '{username}' not found.")


class UserNotAdminError(Exception):
    """Exception raised when a user is not an admin."""

    pass

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User '{username}' does not have admin access.")

    def __str__(self):
        return f"User '{self.username}' does not have admin access."
