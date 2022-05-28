from xml.dom import NotFoundErr
from database.connect import engine

class Alligator():

    _all = [(1, "Barry", 4),
            (2, "Leonie", 2)]

    @staticmethod
    def get_all():
        with engine.connect() as conn:
            results = conn.execute("SELECT * FROM alligator")
            return [Alligator(*a) for a in results]

    @staticmethod
    def get_one_by_id(id):
        with engine.connect() as conn:
            result = conn.execute("SELECT * FROM alligator WHERE id = :id",
                                  id=id).fetchone()
        if not result:
            raise NotFoundErr
        return Alligator(**result)

    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __repr__(self):
        return f"{self.name}, an alligator"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }