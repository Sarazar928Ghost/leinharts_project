from utils.consolecolor import ConsoleColor
from classes.player import Player
from utils.inpututils import cant_be_blank
from typing import Optional


def show_menu_players() -> str:
    ConsoleColor.print_warning("Liste des functions pour les acteurs :")
    return input("1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Retour en arrière\n")


def choose_player() -> str:
    ConsoleColor.print_warning("Choisissez un acteur par son id :")
    return input("Appuyer sur enter si vous voulez retourner en arrière\n")


def update_ranking(first_name) -> Optional[int]:
    ConsoleColor.print_warning("Appuyez sur enter pour retourner en arrière")
    response = "usless"
    while response != "" and not response.isnumeric():
        response = input(f"Rentrez le nouveau classement de {first_name} : ")

    if response == "":
        return None

    return int(response)


def create_player(id: int) -> Player:
    first_name = cant_be_blank("First Name : ")
    last_name = cant_be_blank("Last Name : ")
    birth_day = cant_be_blank("Birth Day (Year/Month/Day) : ")
    sex = cant_be_blank("Sex [Man , Women or Non-Binaire] : ")

    sex = sex.lower()
    while sex != "man" and sex != "women" and sex != "non-binaire":
        ConsoleColor.print_fail("Le sex doit être l'un de ces paramètre : [Man, Women or Non-Binaire]")
        sex = input("Sex [Man, Women, Non-Binaire] : ")
    sex = "Non-Binaire" if sex == "non-binaire" else sex.capitalize()
    ranking = cant_be_blank("Ranking : ")

    while not ranking.isnumeric():
        ranking = cant_be_blank("Ranking ( Must be a int ) : ")

    return Player(id, first_name, last_name, birth_day, sex, int(ranking))


def show_players(players: list) -> None:
    message = ""
    for player in players:
        message += "  {} - {}, {}, {}, {}, {}".format(player.id, *player.serialize().values())
        message += "\n"
    ConsoleColor.print_success("| -------------------------------------------------------- |")
    ConsoleColor.print_success("| ID - First Name , Last Name , Birth Date , Sex , Ranking |")
    print(message)
    ConsoleColor.print_success("| -------------------------------------------------------- |")
