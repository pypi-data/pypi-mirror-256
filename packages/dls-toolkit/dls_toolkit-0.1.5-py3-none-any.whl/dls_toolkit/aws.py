import datetime
from typing import Generator, Optional, Tuple

import boto3  # type: ignore
from dateutil.relativedelta import relativedelta  # type: ignore


def get_last_n_months_date_range(
    number_of_months: int,
) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Get the date range for the last n months.

    Args:
        number_of_months (int): The number of months to go back.

    Returns:
        Tuple[datetime.datetime, datetime.datetime]: A tuple containing the start and end dates of the date range.
    """
    today = datetime.datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    end_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_date = today - relativedelta(months=number_of_months)
    return start_date, end_date


def get_monthly_bill_amount(
    number_of_months: int = 1, account_id: Optional[str] = None
) -> Generator[dict, None, None]:
    """
    Retrieves the monthly bill amount for a specified number of months.

    Args:
        number_of_months (int, optional): The number of months to retrieve the bill amount for. Defaults to 1.
        account_id (str, optional): The account ID to filter the bill amount by. Defaults to None.

    Yields:
        dict: The monthly bill amount. The dictionary contains the date and the amount.

    """
    filters = {}
    ce_client = boto3.client("ce")

    start_date, end_date = get_last_n_months_date_range(number_of_months)

    # Convert dates to strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    if account_id:
        filters = {"Dimensions": {"Key": "LINKED_ACCOUNT", "Values": [account_id]}}

    request_parameters = {
        "TimePeriod": {"Start": start_date_str, "End": end_date_str},
        "Granularity": "MONTHLY",
        "Metrics": ["UnblendedCost"],
    }
    if filters:
        request_parameters["Filter"] = filters

    response = ce_client.get_cost_and_usage(**request_parameters)
    for result in response["ResultsByTime"]:
        yield {
            "date": result["TimePeriod"]["Start"],
            "amount": float(result["Total"]["UnblendedCost"]["Amount"]),
        }
