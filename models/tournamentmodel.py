from classes.tournament import Tournament
from models.model import Model
from models.playermodel import PlayerModel
from tinydb.table import Document
from classes.round import Round
from typing import Optional


class TournamentModel(Model):

    def __init__(self):
        super().__init__("tournament")

    @staticmethod
    def unserialize_many(tournaments_document: list[Document]) -> list[Tournament]:
        player_model = PlayerModel()
        return [TournamentModel.unserialize_single(tournament, player_model)
                for tournament in tournaments_document]

    @staticmethod
    def unserialize_single(tournament: Document, player_model=None) -> Tournament:
        if player_model is None:
            player_model = PlayerModel()

        return Tournament(tournament.doc_id,
                          tournament["name"],
                          tournament["location"],
                          tournament["date"],
                          tournament["numbers_of_turns"],
                          tournament["max_players"],
                          tournament["description"],
                          [[player_model.get(player[0]), player[1]] for player in tournament["players"]],
                          {int(k): v for k, v in tournament["already_played"].items()},
                          tournament["control_of_time"],
                          TournamentModel.unserialize_round(tournament["rounds"])
                          )

    @staticmethod
    def unserialize_round(rounds: list[dict]) -> list[Round]:
        result_rounds = []
        for round in rounds:
            r = Round(round["name"],
                      tuple(
                          [([match[0][0], match[0][1]],
                            [match[1][0], match[1][1]])
                           for match in round["matches"]]
                      )
                      )
            r.start_hour = round["start_hour"]
            r.start_date = round["start_date"]
            r.end_date = round["end_date"]
            r.end_hour = round["end_hour"]
            result_rounds.append(r)
        return result_rounds

    def all(self) -> list[Tournament]:
        tournaments = super().all()
        return self.unserialize_many(tournaments)

    def get(self, id) -> Optional[Tournament]:
        tournament = super().get(id)
        if tournament is not None:
            tournament = self.unserialize_single(tournament)
        return tournament
