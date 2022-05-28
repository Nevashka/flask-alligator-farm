from database.connect import conn
from xml.dom import NotFoundErr

class Alligator():

    @staticmethod
    def get_all():
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM alligator")
            results = curs.fetchall()
        return [Alligator(*a) for a in results] if results else []

    @staticmethod
    def get_one_by_id(id):

        statement = """
            SELECT *
            FROM alligator
            WHERE id = %s
            LIMIT 1;
        """
        with conn.cursor() as curs:
            curs.execute(statement, (id,))
            result = curs.fetchall()
        if not result:
            raise NotFoundErr
        return Alligator(*result[0])

    @staticmethod
    def create(name, age):

        statement = "INSERT INTO alligator (name, age) VALUES (%s, %s) RETURNING *;"
        with conn.cursor() as curs:
            curs.execute(statement, (name, age))
            result = curs.fetchone()
            conn.commit()
            return Alligator(*result)

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