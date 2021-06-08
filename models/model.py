from tinydb import TinyDB
from tinydb.table import Document
from typing import Optional


class Model:

    def __init__(self, table="_default") -> None:
        self.db = TinyDB("data.json")
        self.table = self.db.table(table)

    def insert(self, classes) -> None:
        self.table.insert(Document(classes.serialize(), doc_id=classes.id))

    def truncate(self) -> None:
        self.table.truncate()

    def multiple_insert(self, classes_array: list) -> None:
        for classes in classes_array:
            self.insert(classes)

    def all(self) -> list[Document]:
        return self.table.all()

    def get(self, id) -> Optional[Document]:
        return self.table.get(doc_id=int(id))
