from tinydb import TinyDB
from tinydb.table import Document


class Model:

    def __init__(self, table="_default"):
        self.db = TinyDB("data.json")
        self.table = self.db.table(table)

    def insert(self, classes):
        self.table.insert(Document(classes.serialize(), doc_id=classes.id))

    def truncate(self):
        self.table.truncate()

    def multiple_insert(self, entity_array):
        for entity in entity_array:
            self.insert(entity)

    def all(self):
        return self.table.all()

    def get(self, id):
        return self.table.get(doc_id=int(id))
