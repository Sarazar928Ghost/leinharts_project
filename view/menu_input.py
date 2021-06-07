from classes.player import Player


def show_menu() -> str:
    return input("Liste des functions :\n"
                 "1: Liste de tous les acteurs\n"
                 "2: Liste de tous les tournois\n"
                 "3: Créer un nouveau acteur\n"
                 "4: Stop le programme\n")


def show_menu_players() -> str:
    return input("Liste des functions pour les acteurs :\n"
                 "1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Retour en arrière\n")


def show_menu_tournament() -> str:
    return input("Liste des functions pour ce tournoi :\n"
                 "1: Afficher par ordre alphabétique les acteurs\n"
                 "2: Afficher par ranking les acteurs\n"
                 "3: Afficher les tours\n"
                 "4: Afficher les matchs\n"
                 #todo add a player
                 "5: Retourner au menu principal\n")


def choose_tournament() -> str:
    return input("Choisissez un tournoi par son id :\n"
                 "Appuyer sur enter si vous voulez retourner en arrière\n")


def create_player(id) -> Player:
    first_name = input("First Name : ")
    last_name = input("Last Nae : ")
    birth_day = input("Birth Day (Year/Month/Day) : ")
    sex = input("Sex (Man or Women or Non-Binaire) : ")
    ranking = input("Ranking : ")

    while not ranking.isnumeric():
        ranking = input("Ranking ( Must be a int ) : ")

    print("L'acteur a été crée avec succés.")

    return Player(id, first_name, last_name, birth_day, sex, int(ranking))
