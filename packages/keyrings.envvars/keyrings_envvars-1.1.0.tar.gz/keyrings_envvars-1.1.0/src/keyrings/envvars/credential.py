"""Credentials used by the keyrings.envvars backend."""

import os

from keyring.credentials import Credential


class EnvvarCredential(Credential):
    """
    Read credentials from the environment.

    This is similar to keyring.credentials.EnvironCredential except that it doesn't throw if a variable is unset or
    empty since a service could legitimately use only a username or only a password (for example, an API token)
    """

    def __init__(self, user_env_var: str, pass_env_var: str) -> None:
        self._user_env_var = user_env_var
        self._pass_env_var = pass_env_var

    def __eq__(self, other: object) -> bool:
        """Compare this credential to another."""
        return vars(self) == vars(other)

    def __hash__(self) -> int:
        """Get hash code for dict lookup."""
        return hash((self._user_env_var, self._pass_env_var))

    @property
    def username(self) -> str:
        """Get the username for this credential from the environment."""
        return os.environ.get(self._user_env_var, '')

    @property
    def password(self) -> str:
        """Get the password for this credential from the environment."""
        return os.environ.get(self._pass_env_var, '')
