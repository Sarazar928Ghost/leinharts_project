from player import Player
from models.model import Model


class PlayerModel(Model):

    def __init__(self):
        super().__init__("players")

    @staticmethod
    def unserialize(players_array):
        return [Player(player.doc_id, player["first_name"], player["last_name"], player["birth_date"], player["sex"],
                       player["ranking"])
                for player in players_array]
