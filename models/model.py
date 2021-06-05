from tinydb import TinyDB
from tinydb.table import Document


class Model:

    def __init__(self, table="_default"):
        self.db = TinyDB("data.json")
        self.table = self.db.table(table)

    def insert(self, entity):
        self.table.insert(Document(entity.store(), doc_id=entity.id))

    def truncate(self):
        self.table.truncate()

    def multiple_insert(self, entity_array):
        for entity in entity_array:
            self.insert(entity)

    def all(self):
        return self.table.all()

    def get(self, id):
        return self.table.get(doc_id=id)
