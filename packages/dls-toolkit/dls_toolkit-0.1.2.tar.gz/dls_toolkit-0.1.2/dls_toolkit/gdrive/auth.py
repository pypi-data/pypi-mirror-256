import os
from enum import Enum
from pathlib import Path
from typing import Union

from googleapiclient.discovery import build  # type: ignore


class Role(Enum):
    """
    Represents the roles that can be assigned to users in a Google Drive file.
    """

    WRITER = "writer"
    READER = "reader"
    ORGANIZER = "organizer"
    FILE_ORGANIZER = "fileOrganizer"
    COMMENTER = "commenter"


def authenticate(service_account_path: Union[None, Path, str] = None):
    """
    Authenticates the Google Drive API using the provided service account credentials.
    If no credentials are provided, the function will check for the GOOGLE_APPLICATION_CREDENTIALS
    environment variable. If the environment variable is not set, the function will raise a
    ValueError.

    Args:
        service_account_path (Union[None, Path, str], optional): Path to the service account credentials JSON file. Defaults to None.

    Raises:
        ValueError: If no credentials are provided.

    Returns:
        None: If the authentication is successful.
    """
    env_key = "GOOGLE_APPLICATION_CREDENTIALS"
    if env_key in os.environ:
        return None
    elif service_account_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(service_account_path)
    else:
        raise ValueError("No credentials provided")


def share(file_id: str, email: str, role: Role):
    """
    Share a file with a user by granting them a specific role.

    Args:
        file_id (str): The ID of the file to be shared.
        email (str): The email address of the user to share the file with.
        role (Role): The role to be granted to the user.

    Returns:
        None
    """
    service = build("drive", "v3")
    permission = {"type": "user", "role": role.value, "emailAddress": email}
    service.permissions().create(fileId=file_id, body=permission).execute()
