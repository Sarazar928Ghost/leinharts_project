class Player:
    def __init__(self, id: int, first_name: str, last_name: str, birth_date: str, sex: str, ranking: int) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.ranking = ranking

    def serialize(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "sex": self.sex,
            "ranking": self.ranking,
        }
