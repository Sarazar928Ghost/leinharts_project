def show_players_by_ranking(players: list) -> None:
    players.sort(key=lambda player: player.ranking)
    show_players(players)


def show_players_by_alphabetical(players: list) -> None:
    players.sort(key=lambda player: player.first_name)
    show_players(players)


def show_players(players: list) -> None:
    message = ""
    for player in players:
        message += "{} - {}, {}, {}, {}, {}".format(player.id, *player.serialize().values())
        message += "\n"
    print("ID - First Name , Last Name , Birth Date , Sex , Ranking")
    print(message)
