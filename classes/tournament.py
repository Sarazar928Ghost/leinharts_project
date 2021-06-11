from classes.player import Player
from classes.round import Round


# todo control_of_time
class Tournament:
    def __init__(self,
                 id: int,
                 name: str,
                 location: str,
                 date: str,
                 numbers_of_turns=4,
                 max_players=8,
                 description="",
                 players=None,
                 control_of_time=None,
                 rounds=None) -> None:
        if players is None:
            players: list[Player] = []
        if rounds is None:
            rounds: list[Round] = []
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = numbers_of_turns
        self.max_players = max_players
        self.description = description
        self.players = players
        self.players_id = [player.id for player in players]
        self.control_of_time = control_of_time
        self.rounds = rounds
        self.current_players = len(players)  # For create Round

    @staticmethod
    def sorted_by_ranking(players) -> None:
        players.sort(key=lambda player: player.ranking)

    @staticmethod
    def sorted_by_alphabetical(players) -> None:
        players.sort(key=lambda player: player.first_name)

    @staticmethod
    def sorted_by_id(players) -> None:
        players.sort(key=lambda player: player.id)

    def create_pairs(self) -> list[list[Player, Player]]:
        Tournament.sorted_by_ranking(self.players)
        slice = int(self.current_players / 2)
        return [list(pair) for pair in zip(self.players[slice:], self.players[:slice])]

    def add_round(self, name) -> None:
        self.rounds.append(Round(name, self.create_pairs()))

    def add_player(self, player: Player) -> bool:
        if self.is_full():
            return False
        if player.id in self.players_id:
            return False
        self.current_players += 1
        self.players_id.append(player.id)
        self.players.append(player)
        return True

    def add_players(self, players: list[Player]) -> tuple[list, int, bool]:
        # tuple[list of id OK, int of id KO, bool]
        id = []
        for player in players:
            if not self.add_player(player):
                return id, player.id, False
            id.append(player.id)
            if len(self.players) == 8:
                return id, 0, True
        return id, 0, True

    def set_description(self, description: str) -> None:
        self.description = description

    def set_control_of_time(self, cot: str) -> None:
        self.control_of_time = cot

    def is_full(self) -> bool:
        if self.current_players == self.max_players:
            return True
        return False

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "numbers_of_turns": self.number_of_turns,
            "max_players": self.max_players,
            "description": self.description,
            "players": self.players_id,
            "control_of_time": self.control_of_time,
            "rounds": [round.serialize() for round in self.rounds]
        }
