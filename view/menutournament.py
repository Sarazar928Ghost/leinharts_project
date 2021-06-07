def show_all_tournaments(tournaments) -> None:
    message = ""
    for tournament in tournaments:
        td = list(tournament.serialize().values())
        message += f"{tournament.id} - " \
                   f"{td[0]}, " \
                   f"{td[1]}, " \
                   f"{td[2]}, " \
                   f"{td[3]}, " \
                   f"{td[4]}, " \
                   f"{td[6]}"
        message += "\n"
    print("ID - Name , Location , Date , Numbers of Turns , Description , Control Of Time")
    print(message)


def show_all_rounds(rounds) -> None:
    message = ""
    for idx, round in enumerate(rounds):
        message += "{} - {}, {}, {}, {}, {}".format(idx, *round.serialize().values())
        message += "\n"
    print("ID - Name , Date Start , DateTime Start , Date End , DateTime End")
    print(message)


def show_all_matches(matches) -> None:
    message = ""
    for idx, match in enumerate(matches):
        message += "{} - {}, {}, {}".format(idx, match[0], match[1][0].first_name, match[1][1].first_name)
        message += "\n"
    print(message)
