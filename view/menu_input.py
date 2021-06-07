from utils.consolecolor import ConsoleColor


def show_menu() -> str:
    ConsoleColor.print_warning("Liste des functions :")
    return input("1: Liste de tous les acteurs\n"
                 "2: Liste de tous les tournois\n"
                 "3: Créer un nouveau acteur\n"
                 "4: Stop le programme\n")
