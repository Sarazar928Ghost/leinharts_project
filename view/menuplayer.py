from utils.consolecolor import ConsoleColor
from utils.inpututils import cant_be_blank, must_be_date
from typing import Optional


def show_menu_players() -> str:
    ConsoleColor.print_warning("Liste des functions pour les acteurs :")
    return input("1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Appuyer sur enter pour retourner en arrière\n")


def choose_player() -> str:
    ConsoleColor.print_warning("Choisissez un acteur par son id :")
    return input("Appuyer sur enter si vous voulez retourner en arrière\n")


def update_ranking(first_name) -> Optional[int]:
    ConsoleColor.print_warning("Appuyer sur enter pour retourner en arrière")
    response = "usless"
    while response != "" and not response.isdecimal():
        response = input(f"Rentrer le nouveau classement de {first_name} : ")

    if response == "":
        return None

    return int(response)


def create_player(id: int) -> dict:
    first_name = cant_be_blank("First Name : ")
    last_name = cant_be_blank("Last Name : ")
    birth_day = must_be_date("Birth Day (Year/Month/Day) : ")
    sex = cant_be_blank("Sex [Man , Women or Non-Binaire] : ")

    sex = sex.lower()
    while sex not in ["man", "women", "non-binaire"]:
        ConsoleColor.print_fail("Le sex doit être l'un de ces paramètre : [Man, Women or Non-Binaire]")
        sex = input("Sex [Man, Women, Non-Binaire] : ")
    sex = "Non-Binaire" if sex == "non-binaire" else sex.capitalize()
    ranking = cant_be_blank("Ranking : ")

    while not ranking.isdecimal():
        ranking = cant_be_blank("Ranking ( Must be a int ) : ")

    return {
        "id": id,
        "first_name": first_name,
        "last_name": last_name,
        "birth_day": birth_day,
        "sex": sex,
        "ranking": int(ranking)
    }


def show_players(players: list) -> None:
    message = ""
    for player in players:
        message += f"  {player}"
        message += "\n"
    ConsoleColor.print_success("| -------------------------------------------------------- |")
    ConsoleColor.print_success("| ID - First Name , Last Name , Birth Date , Sex , Ranking |")
    print(message)
    ConsoleColor.print_success("| -------------------------------------------------------- |")
