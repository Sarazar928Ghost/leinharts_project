def show_players_by_ranking(players):
    players.sort(key=lambda player: player.ranking)
    show_players(players)


def show_players_by_alphabetical(players):
    players.sort(key=lambda player: player.first_name)
    show_players(players)


def show_players(players):
    message = ""
    for player in players:
        message += "{} - {}, {}, {}, {}, {}".format(player.id, *player.store().values())
        message += "\n"
    print(message)
