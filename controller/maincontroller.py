from classes.tournament import Tournament
from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
import view.menu_input as menu_input
import view.menuplayer as menu_player
import view.menutournament as menu_tournament
from typing import Optional
from utils.consolecolor import ConsoleColor


class MainController:
    def __init__(self) -> None:
        self.player_model = PlayerModel()
        self.tournament_model = TournamentModel()
        self.players = PlayerModel.unserialize_many(self.player_model.all())
        self.tournaments = TournamentModel.unserialize_many(self.tournament_model.all())

    def menu(self) -> None:
        while True:
            response = menu_input.show_menu()
            # List of players
            if response == "1":
                response = menu_player.show_menu_players()
                if response == "1":
                    Tournament.sorted_by_alphabetical(self.players)
                    menu_player.show_players(self.players)
                elif response == "2":
                    Tournament.sorted_by_ranking(self.players)
                    menu_player.show_players(self.players)
            # List of tournaments
            elif response == "2":
                menu_tournament.show_all_tournaments(self.tournaments)
                tournament = self.get_tournament()
                if tournament is not None:
                    while True:
                        response = menu_tournament.show_menu_tournament()
                        if not self.menu_tournament(response, tournament):
                            break
            # Create a player
            elif response == "3":
                id = self.players[len(self.players) - 1].id + 1 if len(self.players) != 0 else 1
                player = menu_player.create_player(id)
                self.players.append(player)
                self.player_model.insert(player)
            else:
                return

    def get_tournament(self) -> Optional[Tournament]:
        while True:
            choose = menu_tournament.choose_tournament()
            if choose != "":
                tournament = self.select_tournament(choose)
                if tournament is not None:
                    return tournament
                else:
                    ConsoleColor.print_fail("Ce tournoi n'éxiste pas...")
            else:
                return None

    def select_tournament(self, id_tournament: str) -> Optional[Tournament]:
        if id_tournament.isnumeric():
            for tournament in self.tournaments:
                if tournament.id == int(id_tournament):
                    return tournament
        return None

    def menu_tournament(self, response: str, tournament: Tournament) -> bool:
        if response == "1":
            Tournament.sorted_by_alphabetical(self.players)
            menu_player.show_players(tournament.players)
            return True
        elif response == "2":
            Tournament.sorted_by_ranking(self.players)
            menu_player.show_players(tournament.players)
            return True
        elif response == "3":
            menu_tournament.show_all_rounds(tournament.rounds)
            return True
        elif response == "4":
            # [{"Round": [[0.0,0.0], [Player, Player]]}, ...]
            matches: list[dict] = []
            for round in tournament.rounds:
                for match in round.matches:
                    matches.append({round.name: match})
            menu_tournament.show_all_matches(matches)
            return True
        return False
