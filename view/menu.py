from utils.consolecolor import ConsoleColor


def show_menu() -> str:
    ConsoleColor.print_warning("Liste des functions :")
    return input("1: Liste de tous les acteurs\n"
                 "2: Liste de tous les tournois\n"
                 "3: Modifier le classement d'un acteur\n"
                 "4: Créer un nouveau acteur\n"
                 "5: Créer un nouveau tournoi\n"
                 "6: Stop le programme\n")


def print_success(message) -> None:
    ConsoleColor.print_success(message + "\n")


def print_fail(message) -> None:
    ConsoleColor.print_fail(message + "\n")
