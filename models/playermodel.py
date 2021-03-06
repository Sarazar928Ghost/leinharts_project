from classes.player import Player
from models.model import Model
from tinydb.table import Document
from typing import Optional


class PlayerModel(Model):

    def __init__(self) -> None:
        super().__init__("players")

    @staticmethod
    def unserialize_many(players_document: list[Document]) -> list[Player]:
        return [PlayerModel.unserialize_single(player)
                for player in players_document]

    @staticmethod
    def unserialize_single(player: Document) -> Player:
        return Player(player.doc_id, player["first_name"], player["last_name"], player["birth_date"], player["sex"],
                      player["ranking"])

    def all(self) -> list[Player]:
        players = super().all()
        return self.unserialize_many(players)

    def get(self, id) -> Optional[Player]:
        player = super().get(id)
        if player is not None:
            player = self.unserialize_single(player)
        return player
