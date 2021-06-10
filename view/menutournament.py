from utils.consolecolor import ConsoleColor
from classes.tournament import Tournament
from typing import Optional
from utils.inpututils import cant_be_blank


def show_menu_tournament(tournament_name) -> str:
    ConsoleColor.print_warning(f"Liste des functions pour {tournament_name} :")
    return input("1: Afficher par ordre alphabétique les acteurs\n"
                 "2: Afficher par ranking les acteurs\n"
                 "3: Afficher les tours\n"
                 "4: Ajouter un acteur\n"
                 "5: Ajouter plusieurs acteurs\n"
                 "6: Générer le premier tour ( Besoin de 8 acteurs )\n"
                 "7: Retourner au menu principal\n")

def show_menu_round(round_name) -> str:
    ConsoleColor.print_warning(f"Liste des functions pour {round_name} :")
    return input("1: Afficher les match de ce round\n"
                 "2: todo\n")

def choose_round() -> str:
    ConsoleColor.print_warning("Choisissez un tour par son id :")
    return input("Appuyer sur enter si vous voulez retourner en arrière\n")


def choose_tournament() -> str:
    ConsoleColor.print_warning("Choisissez un tournoi par son id :")
    return input("Appuyer sur enter si vous voulez retourner en arrière\n")


def error_not_found_tournament() -> None:
    ConsoleColor.print_fail("Ce tournoi n'éxiste pas...")


def add_player() -> Optional[int]:
    ConsoleColor.print_warning("Appuyez sur enter pour quitter")
    id = input("Rentrez l'id de l'acteur a ajouter ( Example : 10 ) : ")
    if id == "":
        return None
    while not id.isdecimal():
        id = input("L'id doit être un nombre : ")
    return int(id)


def add_players() -> list[int]:
    done = False
    while not done:
        done = True
        response = input("Rentrez les id des acteurs a ajouter ( Example : 1,2,3,4,5 ) : ")
        split_id = response.split(",")
        for idx, id in enumerate(split_id):
            id = id.strip()  # remove space
            if not id.isdecimal():
                done = False
                ConsoleColor.print_fail("Les id doivent être numéric et séparé par des virgules.")
                break
            split_id[idx] = int(id)
    return split_id


def create_tournament(id: int) -> Tournament:
    name = cant_be_blank("Name : ")
    location = cant_be_blank("Location : ")
    date = cant_be_blank("Date (Year/Month/Day) : ")
    numbers_of_turns = "usless"
    while numbers_of_turns != "" and not numbers_of_turns.isdecimal():
        numbers_of_turns = input("numbers_of_turns (Default 4) : ")
    if numbers_of_turns == "":
        numbers_of_turns = 4

    control_of_time = input("Control du temps [bullet, blitz, coup rapide] : ")

    control_of_time = control_of_time.lower()
    while control_of_time != "bullet" and control_of_time != "blitz" and control_of_time != "coup rapide":
        ConsoleColor.print_fail("Control du temps doit être l'un de ces paramètre : [bullet, blitz, coup rapide]")
        control_of_time = input("Control du temps [bullet, blitz, coup rapide] : ")

    description = input("Description : ")

    return Tournament(id, name, location, date, int(numbers_of_turns), description, None, control_of_time)


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
    for match in matches:
        message += "  [{}, {}({})] VS [{}, {}({})]" \
            .format(match[0][0],
                    match[1][0].first_name,
                    match[1][0].id,
                    match[0][1],
                    match[1][1].first_name,
                    match[1][1].id)
        message += "\n"
    ConsoleColor.print_success("| -------------------------------------------------- |")
    ConsoleColor.print_success("| [SCORE, first_name(id)] VS [SCORE, first_name(id)] |")
    print(message)
    ConsoleColor.print_success("| -------------------------------------------------- |")
