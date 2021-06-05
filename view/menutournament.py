def show_all_tournaments(tournaments):
    message = ""
    for tournament in tournaments:
        message += "{} - {}, {}, {}, {}, {}, {}, {}, {}".format(tournament.id, *tournament.store().values())
        message += "\n"
    print(message)


def show_all_rounds(rounds):
    message = ""
    for idx, round in enumerate(rounds):
        message += "{} - {}, {}, {}, {}, {}, {}".format(idx, *round.store().values())
        message += "\n"
    print(message)

# todo
def show_all_matches(matches):
    message = ""
    for idx, match in enumerate(matches):
        message += "{} - {}, {}, {}, {}, {}, {}".format(idx, *match)
        message += "\n"
    print(message)
