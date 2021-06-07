from utils.consolecolor import ConsoleColor
from classes.tournament import Tournament


def show_menu_tournament() -> str:
    ConsoleColor.print_warning("Liste des functions pour ce tournoi :")
    return input("1: Afficher par ordre alphabétique les acteurs\n"
                 "2: Afficher par ranking les acteurs\n"
                 "3: Afficher les tours\n"
                 "4: Afficher les matchs\n"
                 # todo add a player
                 "5: Retourner au menu principal\n")


def choose_tournament() -> str:
    ConsoleColor.print_warning("Choisissez un tournoi par son id :")
    return input("Appuyer sur enter si vous voulez retourner en arrière\n")


def create_tournament(id: int) -> Tournament:
    # todo
    pass


def show_all_tournaments(tournaments: list) -> None:
    message = ""
    for tournament in tournaments:
        td = list(tournament.serialize().values())
        # 1 - test tournament, Belgique, 2021/06/06, 4, Une description pour le test, None
        message += f"  {tournament.id} - " \
                   f"{td[0]}, " \
                   f"{td[1]}, " \
                   f"{td[2]}, " \
                   f"{td[3]}, " \
                   f"{td[4]}, " \
                   f"{td[6]}"
        message += "\n"
    ConsoleColor.print_success("| ------------------------------------------------------------------------------ |")
    ConsoleColor.print_success("| ID - Name , Location , Date , Numbers of Turns , Description , Control Of Time |")
    print(message)
    ConsoleColor.print_success("| ------------------------------------------------------------------------------ |")


def show_all_rounds(rounds: list) -> None:
    message = ""
    for idx, round in enumerate(rounds):
        # 0 - Round x, 2021/06/07, 02:52:02, None, None
        message += "  {} - {}, {}, {}, {}, {}".format(idx, *round.serialize().values())
        message += "\n"
    ConsoleColor.print_success("| ----------------------------------------------------------------- |")
    ConsoleColor.print_success("| ID - Name , Date Start , DateTime Start , Date End , DateTime End |")
    print(message)
    ConsoleColor.print_success("| ----------------------------------------------------------------- |")


def show_all_matches(matches: list[dict]) -> None:
    message = ""
    for round in matches:
        for name, match in round.items():
            # Round x - Match - [0.0, first_name(id)] VS [0.0, first_name(id)]
            message += "  {} - [{}, {}({})] VS [{}, {}({})]" \
                .format(name + " - Match",
                        match[0][0],
                        match[1][0].first_name,
                        match[1][0].id,
                        match[0][1],
                        match[1][1].first_name,
                        match[1][1].id)
            message += "\n"
    ConsoleColor.print_success("| ------------------------------------------------------------------ |")
    ConsoleColor.print_success("| Round - Match - [SCORE, first_name(id)] VS [SCORE, first_name(id)] |")
    print(message)
    ConsoleColor.print_success("| ------------------------------------------------------------------ |")
