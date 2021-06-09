from utils.consolecolor import ConsoleColor
from classes.player import Player
from utils.inpututils import cant_be_blank


def show_menu_players() -> str:
    ConsoleColor.print_warning("Liste des functions pour les acteurs :")
    return input("1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Retour en arrière\n")


def create_player(id: int) -> Player:
    first_name = cant_be_blank("First Name : ")
    last_name = cant_be_blank("Last Name : ")
    birth_day = cant_be_blank("Birth Day (Year/Month/Day) : ")
    sex = cant_be_blank("Sex (Man , Women or Non-Binaire) : ")
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
