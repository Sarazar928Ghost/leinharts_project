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
            players: list[list[Player, float]] = []
        if rounds is None:
            rounds: list[Round] = []
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = numbers_of_turns
        self.max_players = max_players
        self.description = description
        self.players = [player[0] for player in players]
        self.players_id_score = [[player[0].id, player[1]] for player in players]
        self.already_played = {player.id: [] for player in self.players}
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

    def create_round(self, name) -> None:
        slice = int(self.current_players / 2)
        if len(self.rounds) == 0:
            Tournament.sorted_by_ranking(self.players)
            pairs = []
            for pair in zip(self.players[slice:], self.players[:slice]):
                pairs.append((pair[0].id, pair[1].id))
                self.already_played[pair[0].id].append(pair[1].id)
                self.already_played[pair[1].id].append(pair[0].id)
            print(self.already_played)
            self.rounds.append(Round(name, pairs))
            return

        last_round = self.rounds[len(self.rounds) - 1]

        # Round not finish
        if last_round.end_date is None:
            return

        last_matches = last_round.matches
        pid = []
        [[pid.append(player_id_score) for player_id_score in match] for match in last_matches]
        for player_id_score in self.players_id_score:
            for p in pid:
                if p[0] == player_id_score[0]:
                    player_id_score[1] += p[1]
                    break
        pid.sort(key=lambda p: p[1])

        pairs = []
        done = []

        def get_last_pair():
            return [p for p in pid if p[0] not in done]

        for i in range(self.max_players):
            if i == self.max_players - 1 and len(pairs) != 4:
                pair = get_last_pair()
                pairs.append(pair)
                self.already_played[pair[0][0]].append(pair[1][0])
                self.already_played[pair[1][0]].append(pair[0][0])
                break
            if pid[i][0] in done:
                continue
            increment = 1
            pair = [pid[i], pid[i + increment]]
            while True:
                if pair[1][0] in self.already_played[pair[0][0]] or pair[1][0] in done:
                    increment += 1
                    pair[1] = pid[i + increment]
                else:
                    break
            done.append(pid[i][0])
            done.append(pid[i + increment][0])
            self.already_played[pair[0][0]].append(pair[1][0])
            self.already_played[pair[1][0]].append(pair[0][0])
            pair_tuple = tuple(pair)
            pairs.append(pair_tuple)
            pair.clear()
        print(self.already_played)
        print(pairs)
        pairs = tuple(pairs)
        print(last_matches)
        self.rounds.append(
            Round(f"Round {len(self.rounds) + 1}", [], pairs)
        )

    def test(self):
        print(self.already_played)
        last_round = self.rounds[len(self.rounds) - 1]
        last_matches = last_round.matches
        pid = []
        [[pid.append(player_id_score) for player_id_score in match] for match in last_matches]
        for player_id_score in self.players_id_score:
            for p in pid:
                if p[0] == player_id_score[0]:
                    player_id_score[1] += p[1]
                    break
        pid.sort(key=lambda p: p[1])

        pairs = []
        done = []

        def get_last_pair():
            return [p for p in pid if p[0] not in done]

        for i in range(self.max_players):
            if i == self.max_players - 1 and len(pairs) != 4:
                pair = get_last_pair()
                pairs.append(pair)
                self.already_played[pair[0][0]].append(pair[1][0])
                self.already_played[pair[1][0]].append(pair[0][0])
                break
            if pid[i][0] in done:
                continue
            increment = 1
            pair = [pid[i], pid[i + increment]]
            while True:
                if pair[1][0] in self.already_played[pair[0][0]] or pair[1][0] in done:
                    increment += 1
                    pair[1] = pid[i+increment]
                else:
                    break
            done.append(pid[i][0])
            done.append(pid[i+increment][0])
            self.already_played[pair[0][0]].append(pair[1][0])
            self.already_played[pair[1][0]].append(pair[0][0])
            pair_tuple = tuple(pair)
            pairs.append(pair_tuple)
            pair.clear()
        print(self.already_played)
        print(pairs)
        pairs = tuple(pairs)
        print(last_matches)
        self.rounds.append(
            Round(f"Round {len(self.rounds) + 1}", [], pairs)
        )

    def add_player(self, player: Player) -> bool:
        if self.is_full():
            return False
        for players in self.players_id_score:
            if player.id == players[0]:
                return False
        self.current_players += 1
        self.players_id_score.append([player.id, 0.0])
        self.players.append(player)
        if self.is_full():
            self.already_played = {player.id: [] for player in self.players}
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
            "players": self.players_id_score,
            "control_of_time": self.control_of_time,
            "rounds": [round.serialize() for round in self.rounds]
        }

    def __str__(self):
        return f"  {self.id} - " \
               f"{self.name}, " \
               f"{self.location}, " \
               f"{self.date}, " \
               f"{self.number_of_turns}, " \
               f"{self.description}, " \
               f"{self.control_of_time}"
