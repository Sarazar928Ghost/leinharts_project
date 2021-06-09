from utils.consolecolor import ConsoleColor


def cant_be_blank(message, advertissement="Ce champ ne peut pas être vide.") -> str:
    response = input(message)
    while response == "":
        ConsoleColor.print_fail(advertissement)
        response = input(message)
    return response
