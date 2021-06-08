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
                          tournament["description"],
                          [player_model.get(doc_id) for doc_id in tournament["players"]],
                          tournament["control_of_time"],
                          TournamentModel.unserialize_round(tournament["rounds"], player_model)
                          )

    @staticmethod
    def unserialize_round(rounds: list[dict], player_model: PlayerModel) -> list[Round]:
        return [
            Round(round["name"],
                  [],
                  [
                      [match[0], [player_model.get(match[1][0]),
                                  player_model.get(match[1][1])]]
                      for match in round["matches"]
                  ]
                  )
            for round in rounds
        ]

    def all(self) -> list[Tournament]:
        tournaments = super().all()
        return self.unserialize_many(tournaments)

    def get(self, id) -> Optional[Tournament]:
        tournament = super().get(id)
        if tournament is not None:
            tournament = self.unserialize_single(tournament)
        return tournament