from classes.round import Round
from utils.consolecolor import ConsoleColor
from classes.tournament import Tournament
from typing import Optional
from utils.inpututils import cant_be_blank


def show_menu_tournament(tournament_name, number_of_player) -> str:
    ConsoleColor.print_warning(f"Liste des functions pour {tournament_name} :")
    return input("1: Afficher par ordre alphabétique les acteurs\n"
                 "2: Afficher par ranking les acteurs\n"
                 "3: Afficher les tours\n"
                 "4: Afficher tout les match du tournoi\n"
                 "5: Ajouter un acteur\n"
                 "6: Ajouter plusieurs acteurs\n"
                 f"7: Générer un tour ( besoin de {number_of_player} joueurs )\n"
                 "8: Rentrer les scores\n"
                 "9: Voir les scores du tournoi\n"
                 "10: Retourner au menu principal\n")


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
    split_id = []
    while not done:
        done = True
        response = input("Rentrez les id des acteurs a ajouter ( Example : 1,2,3,4,5 ) : ")
        if response.strip() == "":
            return []
        while response[-1] == "," or response[-1] == " ":
            response = response[:-1]
        split_id = response.split(",")
        for idx, id in enumerate(split_id):
            id = id.strip()  # remove space
            if not id.isdecimal():
                done = False
                ConsoleColor.print_fail("Les id doivent être numéric et séparé par des virgules.")
                break
            split_id[idx] = int(id)
    return split_id


def show_scores(players_id_scores) -> None:
    ConsoleColor.print_success("| Name(id) - scores |")
    for p in players_id_scores:
        print(f"  {p[0].first_name}({p[0].id}) - {p[1]}")


def put_scores(round: Round) -> list[int]:
    number_of_matches = len(round.matches)
    scores = []
    ConsoleColor.print_warning("[1 = premier acteur gagne] ; [2 = deuxième acteur gagne] ; [0 = égalité]")
    for i in range(number_of_matches):
        score = "usless"
        while not score.isnumeric() or score not in ["1", "2", "0"]:
            score = cant_be_blank(
                f"Rentrez le score pour ce match ({round.matches[i][0][0]} - {round.matches[i][1][0]}) : "
            )
        scores.append(int(score))
    return scores


def create_tournament(id: int) -> dict:
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
    while control_of_time not in ["bullet", "blitz", "coup rapide"]:
        ConsoleColor.print_fail("Control du temps doit être l'un de ces paramètre : [bullet, blitz, coup rapide]")
        control_of_time = input("Control du temps [bullet, blitz, coup rapide] : ")

    description = input("Description : ")

    return {
        "id": id,
        "name": name,
        "location": location,
        "date": date,
        "numbers_of_turns": int(numbers_of_turns),
        "max_player": 8,
        "description": description,
        "control_of_time": control_of_time
    }


def show_all_tournaments(tournaments: list[Tournament]) -> None:
    message = ""
    for tournament in tournaments:
        message += f"  {tournament}"
        message += "\n"
    ConsoleColor.print_success("| ------------------------------------------------------------------------------ |")
    ConsoleColor.print_success("| ID - Name , Location , Date , Numbers of Turns , Description , Control Of Time |")
    print(message[:-1])
    ConsoleColor.print_success("| ------------------------------------------------------------------------------ |")


def show_all_rounds(rounds: list[Round]) -> None:
    message = ""
    for idx, round in enumerate(rounds):
        message += f"  {idx} - {round}"
        message += "\n"
    ConsoleColor.print_success("| ------------------------------------------------------------------------- |")
    ConsoleColor.print_success("| ID - Name , Date Start , DateTime Start , Date End , DateTime End , Status |")
    print(message[:-1])
    ConsoleColor.print_success("| ------------------------------------------------------------------------- |")


def all_matches_of_round(matches: list[dict]) -> None:
    message = ""
    for match in matches:
        message += "    {} - {}" \
            .format(match[0][0],
                    match[1][0])
        message += "\n"
    ConsoleColor.print_success("| ----------- |")
    ConsoleColor.print_success("|   ID - ID   |")
    print(message[:-1])
    ConsoleColor.print_success("| ----------- |")


def show_all_matches(rounds: list[Round]) -> None:
    message = ""
    for round in rounds:
        message += f"| {round.name} | "
        for match in round.matches:
            message += f"{match[0][0]} - {match[1][0]} | "
        message += "\n"
    ConsoleColor.print_success("| ---------------------------------------------- |")
    print(message[:-1])
    ConsoleColor.print_success("| ---------------------------------------------- | ")
