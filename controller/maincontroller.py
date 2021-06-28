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

    def run(self) -> None:
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
                menu_tournament.show_all_tournaments([str(tournament) for tournament in self.tournaments])
                tournament = self.get_tournament()
                if tournament is not None:
                    while True:
                        response = menu_tournament.show_menu_tournament(tournament.name, tournament.max_players)
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
                        self.player_model.update(self.players)
                        menu.print_success(f"Le ranking de l'acteur {player.first_name} a bien été mis à jour.")
                        break

            # Create a player
            elif response == "4":
                Tournament.sorted_by_id(self.players)
                id = self.players[-1].id + 1 if len(self.players) != 0 else 1
                data_player = menu_player.create_player(id)
                player = Player(*data_player.values())
                self.players.append(player)
                self.player_model.insert(player)
                menu.print_success("L'acteur a été crée avec succés.")
            # Create a tournament
            elif response == "5":
                id = self.tournaments[-1].id + 1 if len(self.tournaments) != 0 else 1
                data_tournament = menu_tournament.create_tournament(id)
                control_of_time = data_tournament.pop("control_of_time")
                tournament = Tournament(*data_tournament.values(), control_of_time=control_of_time)
                self.tournaments.append(tournament)
                self.tournament_model.insert(tournament)
                menu.print_success(f"Le tournoi \"{tournament.name}\" a été crée avec succés.")
            elif response == "6":
                return
            else:
                menu.print_fail("Mauvaise commande.")

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
            length_rounds = len(tournament.rounds) - 1
            if length_rounds == -1 or index_round > length_rounds or index_round < 0:
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

    # Return True for stay in the menu tournament
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
            return True
        # Show all matches of the current tournament
        elif response == "4":
            menu_tournament.show_all_matches(tournament.rounds)
            return True
        # Add one player
        elif response == "5":
            if tournament.is_full():
                menu.print_fail(f"Le tournoi contient déjà {tournament.max_players} acteurs.")
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
                        self.tournament_model.update(self.tournaments)

                        menu.print_success(f"L'acteur \"{player.first_name}\" a été ajouté avec succès.")
                        return True
                menu.print_fail(f"L'acteur avec l'id {id} n'éxiste pas.")
        # Add many players
        elif response == "6":
            if tournament.is_full():
                menu.print_fail(f"Le tournoi contient déjà {tournament.max_players} acteurs.")
                return True
            all_id = menu_tournament.add_players()
            not_found_id = []
            players = []
            for id in all_id:
                done = False
                for player in self.players:
                    if player.id == id:
                        players.append(player)
                        done = True
                        break
                if not done:
                    not_found_id.append(id)

            if len(not_found_id) != 0:
                menu.print_fail(f"Les acteurs avec les id {not_found_id} n'éxistent pas.")

            can_add = tournament.add_players(players)

            self.tournament_model.update(self.tournaments)

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
        elif response == "7":
            if not tournament.is_full():
                menu.print_fail(f"Impossible de crée un Round sans avoir {tournament.max_players} joueurs")
                return True
            if len(tournament.rounds) != 0 and tournament.rounds[-1].end_date is None:
                menu.print_fail(f"Le round \"{tournament.rounds[-1].name}\" n'est pas encore fini.")
                return True
            if len(tournament.rounds) == tournament.number_of_turns:
                menu.print_fail("Le tournoi est terminé.")
                menu_tournament.show_scores(tournament.players_id_score)
                return True
            tournament.create_round()
            self.tournament_model.update(self.tournaments)
            menu.print_success("Le tour a bien été crée ainsi que ses match.")
            return True
        # Put scores
        elif response == "8":
            if len(tournament.rounds) == 0:
                menu.print_fail("Le tournoi ne contient pas encore de round.")
                return True
            round = tournament.rounds[-1]
            if round.end_date is not None:
                menu.print_fail("Le round est déjà fini, tout les scores sont inscris.")
                return True
            scores = menu_tournament.put_scores(round)
            for i, match in enumerate(round.matches):
                tournament.put_scores(match, scores[i])
            round.end()
            self.tournament_model.update(self.tournaments)
            if len(tournament.rounds) == tournament.number_of_turns:
                menu.print_success("Le tournoi est terminé.")
                menu_tournament.show_scores(tournament.players_id_score)
            return True
        # Show scores
        elif response == "9":
            menu_tournament.show_scores(tournament.players_id_score)
            return True
        # Stop
        elif response == "10":
            return False
        return True
