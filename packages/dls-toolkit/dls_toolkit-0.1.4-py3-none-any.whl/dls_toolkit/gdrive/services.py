from googleapiclient.discovery import build  # type: ignore


def drive_service():
    """
    Returns a Google Drive service object.

    This function builds and returns a service object for interacting with the Google Drive API.

    Returns:
        service: A service object for interacting with the Google Drive API.
    """
    return build("drive", "v3")


def sheets_service():
    """
    Returns the Google Sheets service object.

    Returns:
        service: The Google Sheets service object.
    """
    return build("sheets", "v4")
