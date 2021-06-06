from classes.tournament import Tournament
from controller.maincontroller import MainController
from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
from datetime import date


def main():
    menu_controller = MainController()
    menu_controller.menu()

    #player_model = PlayerModel()
    #players = PlayerModel.unserialize(player_model.all())

    #tournament = Tournament(1, "test tournament", "Belgique", date.today().strftime("%Y/%m/%d"))
    #tournament.add_players(players)
    #tournament.add_round("Round 1")

    #tournament_model = TournamentModel()

    #tournament_model.truncate()
    #tournament_model.insert(tournament)


if __name__ == '__main__':
    main()
