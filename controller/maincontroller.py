from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
import view.menu_input as menu_input
import view.menuplayer as menu_player
import view.menutournament as menu_tournament


class MainController:
    def __init__(self):
        self.player_model = PlayerModel()
        self.tournament_model = TournamentModel()
        self.players = PlayerModel.unserialize(self.player_model.all())
        self.tournaments = TournamentModel.unserialize(self.tournament_model.all())

    def menu(self):
        while True:
            response = menu_input.show_menu()
            if response == "1":
                response = menu_input.show_menu_players()
                if response == "1":
                    menu_player.show_players_by_alphabetical(self.players)
                elif response == "2":
                    menu_player.show_players_by_ranking(self.players)
            elif response == "2":
                menu_tournament.show_all_tournaments(self.tournaments)
                tournament = self.get_tournament()
                if tournament is not None:
                    response = menu_input.show_menu_tournament()
                    self.menu_tournament(response, tournament)
            elif response == "3":
                return

    def get_tournament(self):
        while True:
            choose = menu_input.choose_tournament()
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
            menu_player.show_players_by_alphabetical(tournament.players)
        elif response == "2":
            menu_player.show_players_by_ranking(tournament.players)
        elif response == "3":
            menu_tournament.show_all_rounds(tournament.rounds)
        elif response == "4":
            matches = []
            for round in tournament.rounds:
                for match in round.matches:
                    matches.append(match)
            menu_tournament.show_all_matches(matches)
