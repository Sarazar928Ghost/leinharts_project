def show_menu():
    return input("Liste des functions :\n"
                 "1: Liste de tous les acteurs\n"
                 "2: Liste de tous les tournois\n"
                 "3: Stop le programme\n")


def show_menu_players():
    return input("Liste des functions pour les acteurs :\n"
                 "1: Afficher par ordre alphabétique\n"
                 "2: Afficher par ranking\n"
                 "3: Retour en arrière\n")


def show_menu_tournament():
    return input("Liste des functions pour ce tournoi :\n"
                 "1: Afficher par ordre alphabétique les acteurs\n"
                 "2: Afficher par ranking les acteurs\n"
                 "3: Afficher les tours\n"
                 "4: Afficher les matchs\n"
                 "5: Retourner au menu principal\n")


def choose_tournament():
    return input("Choisissez un tournoi par son id :\n"
                 "Appuyer sur enter si vous voulez retourner en arrière\n")
