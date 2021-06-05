from classes.tournament import Tournament
from models.model import Model
from models.playermodel import PlayerModel
from tinydb.table import Document
from classes.round import Round


class TournamentModel(Model):

    def __init__(self):
        super().__init__("tournament")

    @staticmethod
    def unserialize(tournaments_data):
        player_model = PlayerModel()
        return [Tournament(tournament.doc_id,
                           tournament["name"],
                           tournament["location"],
                           tournament["date"],
                           tournament["numbers_of_turns"],
                           tournament["description"],
                           PlayerModel.unserialize(
                               [Document(player_model.get(doc_id), doc_id) for doc_id in tournament["players"]]),
                           tournament["control_of_time"],
                           TournamentModel.unserialize_round(tournament["rounds"], player_model)
                           )
                for tournament in tournaments_data]

    @staticmethod
    def unserialize_round(rounds, player_model):
        return [
            Round(round["name"],
                  [
                      [PlayerModel.unserialize([Document(player_model.get(player[0]), player[0])])[0],
                       PlayerModel.unserialize([Document(player_model.get(player[1]), player[1])])[0]]
                      for player in round["pairs"]
                  ]
                  )
            for round in rounds
        ]
