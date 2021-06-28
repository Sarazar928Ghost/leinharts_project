from utils.consolecolor import ConsoleColor
from datetime import datetime


def cant_be_blank(message, warning="Ce champ ne peut pas être vide.") -> str:
    response = input(message)
    while response == "":
        ConsoleColor.print_fail(warning)
        response = input(message)
    return response


def must_be_date(message, format=None, warning=None) -> str:
    format = "%Y/%m/%d" if format is None else format
    warning = "Le format donné est incorrect" if warning is None else warning
    while True:
        try:
            date = cant_be_blank(message)
            datetime.strptime(date, format)
            return date
        except ValueError:
            ConsoleColor.print_fail(warning)
