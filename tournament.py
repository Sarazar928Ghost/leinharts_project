from player import Player
from round import Round


# todo control_of_time
class Tournament:
    def __init__(self,
                 id: int,
                 name: str,
                 location: str,
                 date: str,
                 numbers_of_turns=4,
                 description="",
                 players=None,
                 control_of_time=None,
                 rounds=[]):
        if players is None:
            players: list[Player] = []
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = numbers_of_turns
        self.description = description
        self.players = players
        self.control_of_time = control_of_time
        self.rounds = rounds

    def sorted_by_ranking(self) -> None:
        self.players.sort(key=lambda player: player.ranking, reverse=True)

    def create_pairs(self) -> tuple[tuple[Player, Player]]:
        self.sorted_by_ranking()  # self.players is now sorted
        return [pair for pair in zip(self.players[:4], self.players[4:])]

    def add_round(self, name):
        self.rounds.append(Round(name, self.create_pairs()))

    def add_player(self, player):
        self.players.append(player)

    def add_players(self, players):
        for player in players:
            self.add_player(player)

    def set_description(self, description):
        self.description = description

    def set_control_of_time(self, cot):
        self.control_of_time = cot

    def store(self):
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "numbers_of_turns": self.number_of_turns,
            "description": self.description,
            "players": [player.id for player in self.players],
            "control_of_time": self.control_of_time,
            "rounds": [round.store() for round in self.rounds]
        }
