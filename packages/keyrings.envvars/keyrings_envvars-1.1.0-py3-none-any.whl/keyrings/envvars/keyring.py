"""keyrings.envvars backend."""

from __future__ import annotations

import os
import re
from collections import defaultdict
from typing import TYPE_CHECKING

from keyring.backend import KeyringBackend
from keyring.errors import PasswordDeleteError, PasswordSetError

from .credential import EnvvarCredential

if TYPE_CHECKING:
    from collections.abc import Set as AbstractSet


class EnvvarsKeyring(KeyringBackend):
    """Pip Environment Credentials EnvvarsKeyring."""

    EnvMapping = dict[str, dict[str, EnvvarCredential]]

    priority: int = 1  # type: ignore[assignment]

    def __init__(self) -> None:
        super().__init__()  # type: ignore[no-untyped-call]

    @staticmethod
    def _get_trailing_number(s: str) -> str | None:
        m = re.search(r'^KEYRING_SERVICE_NAME_(\d+)$', s)
        return m.group(1) if m else None

    @staticmethod
    def _get_ids(environ_keys: AbstractSet[str]) -> filter[str]:
        return filter(
            None,
            map(
                EnvvarsKeyring._get_trailing_number,
                sorted(filter(lambda x: 'KEYRING_SERVICE_NAME_' in x, environ_keys)),
            ),
        )

    @classmethod
    def _get_mapping(cls) -> EnvMapping:
        env_ids = EnvvarsKeyring._get_ids(os.environ.keys())

        env_map: EnvvarsKeyring.EnvMapping = defaultdict(dict)

        for env_id in env_ids:
            service_name = os.getenv('KEYRING_SERVICE_NAME_' + env_id, '')
            if not service_name:
                continue

            cred = EnvvarCredential(
                'KEYRING_SERVICE_USERNAME_' + env_id,
                'KEYRING_SERVICE_PASSWORD_' + env_id,
            )

            env_map[service_name][cred.username] = cred

        return env_map

    def get_password(self, service: str, username: str) -> str | None:
        """
        Get the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :rtype: str | None
        """
        cred = self.get_credential(service, username)
        if cred is not None:
            return str(cred.password)
        return None

    def set_password(self, service: str, username: str, password: str) -> None:
        """
        Set the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :param password: service password
        :raises PasswordSetError: error when setting password
        """
        message = 'Environment should not be modified by keyring'
        raise PasswordSetError(message)

    def delete_password(self, service: str, username: str) -> None:
        """
        Delete the password for the username of the service.

        :param service: keyring service
        :param username: service username
        :raises PasswordDeleteError: error when deleting password
        """
        message = 'Environment should not be modified by keyring'
        raise PasswordDeleteError(message)

    def get_credential(
        self,
        service: str,
        username: str | None,
    ) -> EnvvarCredential | None:
        """
        Get the username and password for the service.

        :param service: keyring service
        :param username: service username
        :return: credentials if service/username credentials exist in keyring
        :rtype: EnvvarCredential | None
        """
        creds = EnvvarsKeyring._get_mapping().get(service)
        if not creds:
            return None
        if username is not None:
            return creds.get(username)
        if len(creds) == 1:
            return next(iter(creds.values()))
        return None
