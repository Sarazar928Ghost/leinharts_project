from classes.player import Player
from models.model import Model


class PlayerModel(Model):

    def __init__(self) -> None:
        super().__init__("players")

    @staticmethod
    def unserialize(players_array) -> list[Player]:
        return [Player(player.doc_id, player["first_name"], player["last_name"], player["birth_date"], player["sex"],
                       int(player["ranking"]))
                for player in players_array]
