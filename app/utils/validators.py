from datetime import datetime


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validate_positive_integer(value: str) -> bool:
    return value.isdigit() and int(value) > 0


def validate_budget(value: str) -> bool:
    try:
        return float(value.replace(",", ".")) > 0
    except ValueError:
        return False