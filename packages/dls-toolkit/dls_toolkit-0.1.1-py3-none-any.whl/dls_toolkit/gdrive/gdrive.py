from typing import Any, Dict, Optional

from .auth import Role, share
from .services import drive_service, sheets_service


def create_folder(
    user_email: str, name: str, folder_parent_id: Optional[str] = None
) -> Optional[str]:
    """
    Creates a new folder in Google Drive with the given name and optional parent folder.

    Args:
        user_email (str): The email address of a user to add to the folder (write permission).
        name (str): The name of the folder to be created.
        folder_parent_id (str, optional): The ID of the parent folder. Defaults to None.

    Returns:
        str: The ID of the newly created folder.
    """
    service = drive_service()
    body: Dict[str, Any] = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if folder_parent_id:
        body["parents"] = [folder_parent_id]
    folder = service.files().create(body=body, fields="id").execute()
    folder_id = folder.get("id")

    if folder_id:
        share(folder_id, user_email, Role.WRITER)

    return folder_id


def create_spreadsheet(user_email: str, title: str, folder_id: str) -> Optional[str]:
    """
    Creates a new spreadsheet with the given title and moves it to the specified folder.
    Shares the spreadsheet with the user_email with the role of WRITER.

    Args:
        user_email (str): The email address of the user to share the spreadsheet with.
        title (str): The title of the new spreadsheet.
        folder_id (str): The ID of the folder to move the spreadsheet to.

    Returns:
        str: The ID of the created spreadsheet.

    Raises:
        HttpError: If an error occurs during the creation or sharing of the spreadsheet.
    """

    sheets = sheets_service()
    body = {"properties": {"title": title}}
    spreadsheet = (
        sheets.spreadsheets().create(body=body, fields="spreadsheetId").execute()
    )
    spreadsheet_id = spreadsheet.get("spreadsheetId")

    # Move file to shared drive
    drive = drive_service()
    drive.files().update(
        fileId=spreadsheet_id,
        body={},
        addParents=folder_id,
        removeParents="root",
        supportsAllDrives=True,
    ).execute()

    if spreadsheet_id:
        share(spreadsheet_id, user_email, Role.WRITER)

    return spreadsheet_id
