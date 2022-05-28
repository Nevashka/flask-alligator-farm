from database.connect import engine
from xml.dom import NotFoundErr

class Alligator():

    @staticmethod
    def get_all():
        with engine.connect() as conn:
            results = conn.execute("SELECT * FROM alligator").fetchall()
        return [Alligator(*a) for a in results]

    @staticmethod
    def get_one_by_id(id):

        statement = """
            SELECT *
            FROM alligator
            WHERE id = :id
            LIMIT 1;
        """
        with engine.connect() as conn:
            result = conn.execute(statement, id=id).fetchall()
        if not result:
            raise NotFoundErr
        return Alligator(**result[0])

    @staticmethod
    def create(name, age):

        statement = """
            INSERT INTO alligator
                (name, age)
            VALUES
                (:name, :age);
        """
        with engine.connect() as conn:
            result = conn.execute(statement, name=name, age=age)
            created = Alligator.get_one_by_id(result.lastrowid)
            return created

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