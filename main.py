
from models.tournamentmodel import TournamentModel
from models.playermodel import PlayerModel
from tournament import Tournament
from datetime import datetime
from player import Player
import time


def main():

    tournament_model = TournamentModel()
    player_model = PlayerModel()

    tournaments_bdd = tournament_model.all()
    test = tournament_model.unserialize(tournaments_bdd)

    players_bdd = player_model.all()
    players_bdd = player_model.unserialize(players_bdd)

    tournament = Tournament(1, "first_tournament", "Belgique", datetime.now().strftime("%H:%M:%S"))
    tournament.set_description("Un tournoi de test")

    numbers_of_players = len(players_bdd)
    id = 0 if numbers_of_players == 0 else players_bdd[numbers_of_players - 1].id

    if numbers_of_players == 8:
        print("8/8 Joueurs")
    else :
        print(f"{numbers_of_players}/8 Joueurs")
        first_name = input("First name : ")
        last_name = input("Last name : ")
        birth_date = input("Birth date : ")
        sex = input("Sex : ")
        ranking = input("Ranking : ")
        for _ in range(numbers_of_players, 8):
            id += 1
            players_bdd.append(Player(id, first_name, last_name, birth_date, sex, ranking))

    player_model.truncate()
    player_model.multiple_insert(players_bdd)
    
    tournament.add_players(players_bdd)

    tournament.add_round("Round 1")



    tournament_model.truncate()
    tournament_model.insert(tournament)





if __name__ == '__main__':
    main()
