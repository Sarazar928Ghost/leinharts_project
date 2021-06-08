from utils.consolecolor import ConsoleColor
from classes.player import Player


def show_menu_players() -> str:
    ConsoleColor.print_warning("Liste des functions pour les acteurs :")
    return input("1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Retour en arrière\n")


def create_player(id: int) -> Player:
    first_name = input("First Name : ")
    last_name = input("Last Name : ")
    birth_day = input("Birth Day (Year/Month/Day) : ")
    sex = input("Sex (Man , Women or Non-Binaire) : ")
    ranking = input("Ranking : ")

    while not ranking.isnumeric():
        ranking = input("Ranking ( Must be a int ) : ")

    if first_name == "" or last_name == "" or birth_day == "" or sex == "":
        ConsoleColor.print_fail("Les champs ne peuvent pas être vide")
        create_player(id)

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
