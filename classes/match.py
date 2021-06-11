class Match:
    def __init__(self, players, scores=[0.0, 0.0]):
        self.player_one = [scores[0], players[0]]
        self.player_two = [scores[1], players[1]]

    def serialize(self):
        return {
            "players": [self.player_one[1].id, self.player_two[1].id],
            "scores": [self.player_one[0], self.player_two[0]]
        }