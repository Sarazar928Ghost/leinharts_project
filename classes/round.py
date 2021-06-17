from datetime import datetime


class Round:
    def __init__(self, name: str, matches: tuple = None) -> None:
        self.name = name
        self.start_date = datetime.now().strftime("%Y/%m/%d")
        self.start_hour = datetime.now().strftime("%H:%M:%S")
        self.end_date = None
        self.end_hour = None
        self.matches = matches

    def end(self) -> None:
        self.end_date = datetime.now().strftime("%Y/%m/%d")
        self.end_hour = datetime.now().strftime("%H:%M:%S")

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "start_date": self.start_date,
            "start_hour": self.start_hour,
            "end_date": self.end_date,
            "end_hour": self.end_hour,
            "matches": [[[match[0][0], match[0][1]], [match[1][0], match[1][1]]] for match in self.matches]
        }

    def __str__(self) -> str:
        message = f"{self.name}, {self.start_date}, {self.start_hour}, {self.end_date}, {self.end_hour}"
        if self.end_date is not None:
            message += ", Terminé"
        else:
            message += ", En cours"
        return message
