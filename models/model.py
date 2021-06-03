from tinydb import TinyDB
from tinydb.table import Document


class Model:

    def __init__(self, table="_default"):
        self.db = TinyDB("data.json")
        self.table = self.db.table(table)

    def insert(self, data, doc_id=None):
        if doc_id is None:
            self.table.insert(data)
            return

        self.table.insert(Document(data, doc_id=doc_id))

    def multiple_insert(self, data_array):
        for data in data_array:
            self.insert(data)

    def all(self):
        return self.table.all()

    def get(self, id):
        return self.table.get(doc_id=id)
