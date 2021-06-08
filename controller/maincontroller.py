from classes.tournament import Tournament
from models.playermodel import PlayerModel
from models.tournamentmodel import TournamentModel
import view.menu as menu
import view.menuplayer as menu_player
import view.menutournament as menu_tournament
from typing import Optional


class MainController:
    def __init__(self) -> None:
        self.player_model = PlayerModel()
        self.tournament_model = TournamentModel()
        self.players = self.player_model.all()
        self.tournaments = self.tournament_model.all()

    def menu(self) -> None:
        while True:
            response = menu.show_menu()
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
                menu.print_success("L'acteur a été crée avec succés.")
            # Create a tournament
            elif response == "4":
                id = self.tournaments[len(self.tournaments) - 1].id + 1 if len(self.tournaments) != 0 else 1
                tournament = menu_tournament.create_tournament(id)
                self.tournaments.append(tournament)
                self.tournament_model.insert(tournament)
                menu.print_success("Le tournoi a été crée avec succés.")
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
                    menu.print_fail("Le tournament choisis n'éxiste pas.")
            else:
                return None

    def select_tournament(self, id_tournament: str) -> Optional[Tournament]:
        if id_tournament.isnumeric():
            for tournament in self.tournaments:
                if tournament.id == int(id_tournament):
                    return tournament
        return None

    def menu_tournament(self, response: str, tournament: Tournament) -> bool:
        # Show Players
        if response == "1":
            Tournament.sorted_by_alphabetical(self.players)
            menu_player.show_players(tournament.players)
            return True
        # Show Players
        elif response == "2":
            Tournament.sorted_by_ranking(self.players)
            menu_player.show_players(tournament.players)
            return True
        # Show Rounds
        elif response == "3":
            menu_tournament.show_all_rounds(tournament.rounds)
            return True
        # Show Matches
        elif response == "4":
            # [{"Round": [[0.0,0.0], [Player, Player]]}, ...]
            matches: list[dict] = []
            for round in tournament.rounds:
                for match in round.matches:
                    matches.append({round.name: match})
            menu_tournament.show_all_matches(matches)
            return True
        # Add one player
        elif response == "5":
            if len(tournament.players) == 8:
                menu.print_fail("Le tournoi contient déjà 8 acteurs.")
                return True
            while True:
                id = menu_tournament.add_player()
                if id is None:
                    return True
                for player in self.players:
                    if player.id == id:
                        if not tournament.add_player(player):
                            menu.print_fail(f"L'acteur avec l'id {id} est déjà inscris dans le tournoi.")
                            return True
                        self.tournament_model.truncate()
                        self.tournament_model.multiple_insert(self.tournaments)

                        menu.print_success("L'acteur a été ajouté avec succès.")
                        return True
                menu.print_fail(f"L'acteur avec l'id {id} n'éxiste pas.")
        # Add many players
        elif response == "6":
            if len(tournament.players) == 8:
                menu.print_fail("Le tournoi contient déjà 8 acteurs.")
                return True
            all_id = menu_tournament.add_players()
            done = False
            not_found_id = 0
            players = []
            for id in all_id:
                done = False
                for player in self.players:
                    if player.id == id:
                        players.append(player)
                        done = True
                        break
                # KO
                if not done:
                    not_found_id = id
                    break

            # KO
            if not done:
                menu.print_fail(f"L'acteur avec l'id {not_found_id} n'éxiste pas.")
                return True

            can_add = tournament.add_players(players)
            # KO
            if not can_add[1]:
                menu.print_fail(f"L'acteur avec l'id {can_add[0]} est déjà inscris dans le tournoi.")
                return True

            # OK
            self.tournament_model.truncate()
            self.tournament_model.multiple_insert(self.tournaments)
            menu.print_success("Les acteurs ont été ajouté avec succès.")
            return True
        # Generate a Round
        elif response == "7":
            if len(tournament.players) != 8:
                menu.print_fail("Impossible de crée un Round sans avoir 8 joueurs")
                return True
            if len(tournament.rounds) != 0:
                menu.print_fail("Le tournoi a déjà un tour principal")
                return True
            tournament.add_round("Round 1")
            self.tournament_model.truncate()
            self.tournament_model.multiple_insert(self.tournaments)
            menu.print_success("Le tour a bien été crée ainsi que ses match.")
            return True
        return False
