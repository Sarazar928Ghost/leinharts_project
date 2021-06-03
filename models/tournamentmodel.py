from tournament import Tournament
from models.model import Model
from models.playermodel import PlayerModel
from tinydb.table import Document


class TournamentModel(Model):

    def __init__(self):
        super().__init__("tournament")

    @staticmethod
    def unserialize(tournaments_data):
        return [Tournament(tournament.doc_id,
                           tournament["name"],
                           tournament["location"],
                           tournament["date"],
                           tournament["numbers_of_turns"],
                           tournament["description"],
                           PlayerModel.unserialize([Document(player, doc_id)
                                                    for data in tournament["players"]
                                                    for doc_id, player in data.items()]),
                           tournament["control_of_time"],
                           tournament["rounds"])
                for tournament in tournaments_data]
