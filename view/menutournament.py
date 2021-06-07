def show_all_tournaments(tournaments) -> None:
    message = ""
    for tournament in tournaments:
        td = list(tournament.serialize().values())
        # 1 - test tournament, Belgique, 2021/06/06, 4, Une description pour le test, None
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
        # 0 - Round x, 2021/06/07, 02:52:02, None, None
        message += "{} - {}, {}, {}, {}, {}".format(idx, *round.serialize().values())
        message += "\n"
    print("ID - Name , Date Start , DateTime Start , Date End , DateTime End")
    print(message)


def show_all_matches(matches) -> None:
    message = ""
    for round in matches:
        for name, match in round.items():
            # Round x - Match - [0.0, first_name] VS [0.0, first_name]
            message += "{} - [{}, {}] VS [{}, {}]"\
                .format(name+" - Match", match[0][0], match[1][0].first_name, match[0][1], match[1][1].first_name)
            message += "\n"
    print(message)
