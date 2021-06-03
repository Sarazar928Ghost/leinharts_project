
from models.tournamentmodel import TournamentModel


def main():

    tournament_model = TournamentModel()
    tournament_data = tournament_model.all()
    tournaments = TournamentModel.unserialize(tournament_data)
    tournament = tournaments[0]




if __name__ == '__main__':
    main()
