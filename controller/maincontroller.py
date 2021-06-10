from classes.player import Player
from classes.round import Round
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
                        response = menu_tournament.show_menu_tournament(tournament.name)
                        if not self.menu_tournament(response, tournament):
                            break
            # Update ranking of a player
            elif response == "3":
                Tournament.sorted_by_ranking(self.players)
                menu_player.show_players(self.players)
                player = self.get_player()
                if player is not None:
                    while True:
                        ranking = menu_player.update_ranking(player.first_name)
                        if ranking is None:
                            break
                        player.ranking = ranking
                        self.player_model.truncate()
                        self.player_model.multiple_insert(self.players)
                        menu.print_success(f"Le ranking de l'acteur {player.first_name} a bien été mis à jour.")
                        break

            # Create a player
            elif response == "4":
                Tournament.sorted_by_id(self.players)
                id = self.players[len(self.players) - 1].id + 1 if len(self.players) != 0 else 1
                player = menu_player.create_player(id)
                self.players.append(player)
                self.player_model.insert(player)
                menu.print_success("L'acteur a été crée avec succés.")
            # Create a tournament
            elif response == "5":
                id = self.tournaments[len(self.tournaments) - 1].id + 1 if len(self.tournaments) != 0 else 1
                tournament = menu_tournament.create_tournament(id)
                self.tournaments.append(tournament)
                self.tournament_model.insert(tournament)
                menu.print_success("Le tournoi a été crée avec succés.")
            else:
                return

    def get_round(self, tournament: Tournament) -> Optional[Round]:
        while True:
            choose = menu_tournament.choose_round()
            if choose != "":
                round = self.select_round(choose, tournament)
                if round is not None:
                    return round
                else:
                    menu.print_fail("Le tour choisis n'éxiste pas.")
            else:
                return None

    def select_round(self, index_round: str, tournament: Tournament) -> Optional[Round]:
        if index_round.isdecimal():
            index_round = int(index_round)
            length_rounds = len(tournament.rounds)
            if length_rounds == 0:
                return None
            length_rounds -= 1
            if index_round > length_rounds:
                return None
            if index_round < 0:
                return None
            return tournament.rounds[index_round]

        return None

    def get_player(self) -> Optional[Player]:
        while True:
            choose = menu_player.choose_player()
            if choose != "":
                player = self.select_player(choose)
                if player is not None:
                    return player
                else:
                    menu.print_fail("L'acteur choisis n'éxiste pas.")
            else:
                return None

    def select_player(self, id_player: str) -> Optional[Player]:
        if id_player.isdecimal():
            for player in self.players:
                if player.id == int(id_player):
                    return player
        return None

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
        if id_tournament.isdecimal():
            for tournament in self.tournaments:
                if tournament.id == int(id_tournament):
                    return tournament
        return None

    def menu_tournament(self, response: str, tournament: Tournament) -> bool:
        # Show Players
        if response == "1":
            Tournament.sorted_by_alphabetical(tournament.players)
            menu_player.show_players(tournament.players)
            return True
        # Show Players
        elif response == "2":
            Tournament.sorted_by_ranking(tournament.players)
            menu_player.show_players(tournament.players)
            return True
        # Show Rounds
        elif response == "3":
            menu_tournament.show_all_rounds(tournament.rounds)
            while True:
                round = self.get_round(tournament)
                if round is None:
                    break
                
                response = menu_tournament.show_menu_round(round.name)
                if response == "1":
                    menu_tournament.show_all_matches(round.matches)
                    break
                else:
                    break
            return True
        # Add one player
        elif response == "4":
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

                        menu.print_success(f"L'acteur \"{player.first_name}\" a été ajouté avec succès.")
                        return True
                menu.print_fail(f"L'acteur avec l'id {id} n'éxiste pas.")
        # Add many players
        elif response == "5":
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


            # OK
            can_add = tournament.add_players(players)

            self.tournament_model.truncate()
            self.tournament_model.multiple_insert(self.tournaments)

            if len(can_add[0]) == 0:
                message = f"Aucun acteur n'a été ajouté au tournoi \"{tournament.name}\"."
            else:
                message = "Les acteurs avec les id : ["
                for id in can_add[0]:
                    message += f"{id},"
                message = message[:-1]
                message += f"] ont bien été ajouté au tournoi \"{tournament.name}\"."
            menu.print_success(message)
            if not can_add[2]:
                menu.print_fail(
                    f"L'acteur avec l'id {can_add[1]} est déjà inscris dans le tournoi \"{tournament.name}\"."
                )
            return True
        # Generate a Round
        elif response == "6":
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
