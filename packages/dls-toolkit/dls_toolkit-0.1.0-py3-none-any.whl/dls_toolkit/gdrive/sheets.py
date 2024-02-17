from typing import Any, List, Optional

from .services import sheets_service


def row_count(spreadsheet_id: str, sheet_name: str) -> int:
    """
    Returns the number of rows in a specific sheet of a Google Sheets spreadsheet.

    Note: This function is not efficient for large spreadsheets. It reads cell range A:Z of
    the sheet to count the rows.

    Args:
        spreadsheet_id (str): The ID of the Google Sheets spreadsheet.
        sheet_name (str): The name of the sheet.

    Returns:
        int: The number of rows in the specified sheet.
    """
    service = sheets_service()
    request = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A:Z")
    )
    response = request.execute()
    return len(response["values"])


def write_values(
    spreadsheet_id: str, values: List[List[Any]], range_name: Optional[str] = "A1"
):
    """
    Writes values to a specified range in a Google Sheets spreadsheet.

    Args:
        spreadsheet_id (str): The ID of the spreadsheet.
        values (List[List[Any]]): The values to write to the spreadsheet.
        range_name (str, optional): The range to write the values to. Defaults to "A1".

    Returns:
        dict: The response from the API call.

    Raises:
        HttpError: If an error occurs during the API call.
    """
    service = sheets_service()

    body = {"values": values}
    return (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )
