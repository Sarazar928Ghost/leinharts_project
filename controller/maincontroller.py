from classes.tournament import Tournament
from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
import view.menu_input as menu_input
import view.menuplayer as menu_player
import view.menutournament as menu_tournament
from typing import Optional


class MainController:
    def __init__(self) -> None:
        self.player_model = PlayerModel()
        self.tournament_model = TournamentModel()
        self.players = PlayerModel.unserialize(self.player_model.all())
        self.tournaments = TournamentModel.unserialize(self.tournament_model.all())

    def menu(self) -> None:
        while True:
            response = menu_input.show_menu()
            # List of players
            if response == "1":
                response = menu_input.show_menu_players()
                if response == "1":
                    menu_player.show_players_by_alphabetical(self.players)
                elif response == "2":
                    menu_player.show_players_by_ranking(self.players)
            # List of tournaments
            elif response == "2":
                menu_tournament.show_all_tournaments(self.tournaments)
                tournament = self.get_tournament()
                if tournament is not None:
                    response = menu_input.show_menu_tournament()
                    self.menu_tournament(response, tournament)
            # Create a player
            elif response == "3":
                id = self.players[len(self.players) - 1].id + 1 if len(self.players) != 0 else 1
                player = menu_input.create_player(id)
                self.players.append(player)
                self.player_model.insert(player)
                menu_player.show_players_by_ranking(self.players)
            elif response == "4":
                return

    def get_tournament(self) -> Optional[Tournament]:
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

    def select_tournament(self, id_tournament: str) -> Optional[Tournament]:
        if id_tournament.isnumeric():
            for tournament in self.tournaments:
                if tournament.id == int(id_tournament):
                    return tournament
        return None

    def menu_tournament(self, response: str, tournament: Tournament) -> None:
        if response == "1":
            menu_player.show_players_by_alphabetical(tournament.players)
        elif response == "2":
            menu_player.show_players_by_ranking(tournament.players)
        elif response == "3":
            menu_tournament.show_all_rounds(tournament.rounds)
        elif response == "4":
            # [{"Round": [[0.0,0.0], [Player, Player]]}, ...]
            matches: list[dict] = []
            for round in tournament.rounds:
                for match in round.matches:
                    matches.append({round.name: match})
            menu_tournament.show_all_matches(matches)
