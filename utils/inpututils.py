from utils.consolecolor import ConsoleColor


def cant_be_blank(message, warning="Ce champ ne peut pas être vide.") -> str:
    response = input(message)
    while response == "":
        ConsoleColor.print_fail(warning)
        response = input(message)
    return response
