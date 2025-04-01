import base64
from logging import Logger

from .user_model import UserModel


class PasswordService:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    def verify_password(self, password: str, user_to_verify: UserModel) -> bool:
        """
        The function `verify_password` compares the encoded password input with the hashed password of a
        user to verify if they match.

        :param password: The `password` parameter is a string that represents the password input that
        needs to be verified against the hashed password of a user
        :type password: str
        :param user_to_verify: UserModel(username: str, hashed_password: str)
        :type user_to_verify: UserModel
        :return: a boolean value, which indicates whether the password provided matches the hashed
        password stored for the user being verified.
        """
        self.logger.debug(f"Verifying password for user: {user_to_verify.username}")
        return self.encode_passwords(password) == user_to_verify.hashed_password

    def encode_passwords(password: str) -> str:
        """
        The function `encode_passwords` encodes a given password using base64 encoding.

        :param password: The `encode_passwords` function takes a password as input, encodes it using
        base64 encoding, and returns the encoded password as a string
        :type password: str
        :return: The function `encode_passwords` takes a password as input, encodes it using base64
        encoding, and then decodes the result before returning it as a string.
        """
        return base64.b64encode(password.encode()).decode()
