from classes.player import Player
from classes.round import Round
import random

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
        self.players_id_score = [[player[0], player[1]] for player in players]
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
            self.rounds.append(Round("Round 1", matches))
            return

        if self.rounds[-1].end_date is None:
            return

        self.players_id_score.sort(key=lambda p: (p[1], p[0].ranking))
        copy_pid = self.players_id_score.copy()
        matches = self.generate_matches_advanced(copy_pid)
        self.rounds.append(
            Round(f"Round {len(self.rounds) + 1}", matches)
        )

    def put_scores(self, match):
        for pid in self.players_id_score:
            if pid[0].id == match[0][0]:
                pid[1] = match[0][1]
            if pid[0].id == match[1][0]:
                pid[1] = match[1][1]

    def add_already_played(self, id_1, id_2):
        self.already_played[id_1].append(id_2)
        self.already_played[id_2].append(id_1)

    def __generate_match_valid(self, copy_pid, opponents):
        marge = 0
        next = 0
        use_marge = marge
        while True:
            pidc = copy_pid.copy()
            pid = pidc.pop(next)
            id_pid = pid[0].id
            id_p = 0
            match = []
            matches = []
            for p in pidc:
                id_p = p[0].id
                if id_p not in self.already_played[id_pid]:
                    if use_marge > 0:
                        use_marge -= 1
                        continue
                    match = ([id_pid, pid[1]], [id_p, p[1]])
                    pidc.remove(p)
                    break
            if len(match) == 2:
                matches.append(match)
            done = []
            for k in opponents:
                if len(pidc) == 2 and pidc[0][0].id not in self.already_played[pidc[1][0].id]:
                    m = ([pidc[0][0].id, pidc[0][1]], [pidc[1][0].id, pidc[1][1]])
                    matches.append(m)
                    pidc.clear()
                elif len(opponents[k]) == 1:
                    match = []
                    for p in pidc:
                        if (p[0].id == opponents[k][0] or p[0].id == k) and p[0].id not in done:
                            match.append(p)
                            done.append(p[0].id)
                    if len(match) == 2:
                        if match[0][0].id in self.already_played[match[1][0].id]:
                            done = [1]
                            break
                        pidc.remove(match[0])
                        pidc.remove(match[1])
                        matches.append(([match[0][0].id, match[0][1]], [match[1][0].id, match[1][1]]))
            if len(done) % 2 != 0:
                marge += 1
                if marge >= len(opponents[list(opponents.keys())[0]]):
                    marge = 0
                    next += 1
                if next >= len(pidc):
                    next = 0
                continue
            return matches, done

    def generate_matches_advanced(self, copy_pid):
        opponents = {p.id: [k for k in self.already_played if k != p.id and k not in self.already_played[p.id]]
                     for p in self.players}
        matches = []

        def create_last_match():
            m = ([copy_pid[0][0].id, copy_pid[0][1]], [copy_pid[1][0].id, copy_pid[1][1]])
            self.add_already_played(m[0][0], m[1][0])
            matches.append(m)
            copy_pid.clear()
        while copy_pid:

            pairs, done = self.__generate_match_valid(copy_pid, opponents)
            matches = matches + pairs
            need_remove = []
            for p in copy_pid:
                for pair in pairs:
                    if p[0].id == pair[0][0] or p[0].id == pair[1][0]:
                        need_remove.append(p)
                        break
            for r in need_remove:
                copy_pid.remove(r)
            for p in pairs:
                del opponents[p[0][0]]
                del opponents[p[1][0]]
                if p[0][0] in done:
                    done.remove(p[0][0])
                if p[1][0] in done:
                    done.remove(p[1][0])
                for k in opponents:
                    if p[0][0] in opponents[k]:
                        opponents[k].remove(p[0][0])
                    if p[1][0] in opponents[k]:
                        opponents[k].remove(p[1][0])
                self.add_already_played(p[0][0], p[1][0])

            if opponents:
                for d in done:
                    del opponents[d]
                    [opponents[k].remove(d) for k in opponents if d in opponents[k]]
            for i in range(0, len(done), 2):
                self.add_already_played(done[i], done[i + 1])

            if len(copy_pid) == 2:
                create_last_match()

        return matches

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
