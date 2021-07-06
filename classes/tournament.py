from classes.player import Player
from classes.round import Round


class Tournament:
    def __init__(self,
                 id: int,
                 name: str,
                 location: str,
                 date: str,
                 numbers_of_turns=4,
                 max_players=8,
                 description="",
                 players_id_score=None,
                 already_played=None,
                 control_of_time=None,
                 rounds=None) -> None:
        if players_id_score is None:
            players_id_score: list[list[Player, float]] = []
        if rounds is None:
            rounds: list[Round] = []
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turns = numbers_of_turns
        self.max_players = max_players
        self.description = description
        self.players = [player[0] for player in players_id_score]
        self.players_id_score = players_id_score
        self.already_played = {player.id: [] for player in self.players} if already_played is None else already_played
        self.control_of_time = control_of_time
        self.rounds = rounds
        self.current_players = len(players_id_score)  # For create Round

    @staticmethod
    def sorted_by_ranking(players) -> None:
        players.sort(key=lambda player: player.ranking)

    @staticmethod
    def sorted_by_alphabetical(players) -> None:
        players.sort(key=lambda player: player.first_name)

    @staticmethod
    def sorted_by_id(players) -> None:
        players.sort(key=lambda player: player.id)

    def create_round(self) -> None:
        if len(self.rounds) == self.number_of_turns:
            return
        slice = int(self.current_players / 2)
        if len(self.rounds) == 0:
            self.players_id_score.sort(key=lambda p: p[0].ranking)
            matches = []
            for pair in zip(self.players_id_score[slice:], self.players_id_score[:slice]):
                matches.append(([pair[0][0].id, pair[0][1]], [pair[1][0].id, pair[1][1]]))
                self.add_already_played(pair[0][0].id, pair[1][0].id)
            self.rounds.append(Round("Round 1", tuple(matches)))
            return

        if self.rounds[-1].end_date is None:
            return

        self.players_id_score.sort(key=lambda p: (p[1], p[0].ranking))
        matches = self.generate_matches()
        self.rounds.append(
            Round(f"Round {len(self.rounds) + 1}", tuple(matches))
        )

    def put_scores(self, match, response) -> None:
        if response == 1:
            match[0][1] += 1
        elif response == 2:
            match[1][1] += 1
        elif response == 0:
            match[1][1] += 0.5
            match[0][1] += 0.5
        for pid in self.players_id_score:
            if pid[0].id == match[0][0]:
                pid[1] += match[0][1]
            if pid[0].id == match[1][0]:
                pid[1] += match[1][1]

    def add_already_played(self, id_1, id_2) -> None:
        self.already_played[id_1].append(id_2)
        self.already_played[id_2].append(id_1)

    # -_-'
    def generate_matches(self) -> tuple[tuple[list, list], ...]:
        next = 0
        while True:
            matches = []
            p = self.players.copy()
            done = []
            copy_already_played = self.already_played.copy()
            while p:
                next = 0 if len(p) == 1 else next
                player_one = p.pop(next)
                for player_two in p:
                    if player_two.id not in done \
                            and player_one.id not in done \
                            and player_two.id not in copy_already_played[player_one.id]:
                        matches.append(([player_one.id, 0.0], [player_two.id, 0.0]))
                        done = done + [player_one.id, player_two.id]
                        copy_already_played[player_one.id].append(player_two.id)
                        copy_already_played[player_two.id].append(player_one.id)
                        break
            if len(matches) == 4:
                break
            else:
                next = 1
        self.already_played = copy_already_played
        return tuple(matches)

    def add_player(self, player: Player) -> bool:
        if self.is_full():
            return False
        for players in self.players_id_score:
            if player.id == players[0].id:
                return False
        self.current_players += 1
        self.players_id_score.append([player, 0.0])
        self.players.append(player)
        if self.is_full():
            self.already_played = {player.id: [] for player in self.players}
        return True

    def add_players(self, players: list[Player]) -> tuple[list, int, bool]:
        # tuple[list of id OK, int of id KO, bool OK or KO]
        id = []
        for player in players:
            if not self.add_player(player):
                return id, player.id, False
            id.append(player.id)
            if len(self.players) == self.max_players:
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
            "players": [[pid[0].id, pid[1]] for pid in self.players_id_score],
            "already_played": self.already_played,
            "control_of_time": self.control_of_time,
            "rounds": [round.serialize() for round in self.rounds]
        }

    def __str__(self) -> str:
        return f"  {self.id} - " \
               f"{self.name}, " \
               f"{self.location}, " \
               f"{self.date}, " \
               f"{self.number_of_turns}, " \
               f"{self.description}, " \
               f"{self.control_of_time}"
