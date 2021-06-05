from view.menuplayer import show_players_by_ranking, show_players_by_alphabetical
from view.menutournament import show_all_tournaments, show_all_rounds, show_all_matches
from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
from view.menu import show_menu, show_menu_players, show_menu_tournament, choose_tournament


class MainController:
    def __init__(self):
        self.player_model = PlayerModel()
        self.tournament_model = TournamentModel()
        self.players = PlayerModel.unserialize(self.player_model.all())
        self.tournaments = TournamentModel.unserialize(self.tournament_model.all())

    def menu(self):
        while True:
            response = show_menu()
            if response == "1":
                response = show_menu_players()
                if response == "1":
                    show_players_by_alphabetical(self.players)
                elif response == "2":
                    show_players_by_ranking(self.players)
                input("Press enter for continue...")
            elif response == "2":
                show_all_tournaments(self.tournaments)
                tournament = self.get_tournament()
                if tournament is not None:
                    response = show_menu_tournament()
                    self.menu_tournament(response, tournament)

    def get_tournament(self):
        while True:
            choose = choose_tournament()
            if choose != "":
                tournament = self.select_tournament(choose)
                if tournament is not None:
                    return tournament
                else:
                    print("Ce tournoi n'éxiste pas...")
            else:
                return None

    def select_tournament(self, id_tournament):
        if id_tournament.isnumeric():
            for tournament in self.tournaments:
                if tournament.id == int(id_tournament):
                    return tournament
        return None

    def menu_tournament(self, response, tournament):
        if response == "1":
            show_players_by_alphabetical(tournament.players)
        elif response == "2":
            show_players_by_ranking(tournament.players)
        elif response == "3":
            show_all_rounds(tournament.rounds)
        elif response == "4":
            show_all_matches(tournament.matches)
