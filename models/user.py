from xml.dom import NotFoundErr
from bcrypt import checkpw
from os import environ

from database.connect import conn

class User():

    @staticmethod
    def get_all():
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM user_account")
            results = curs.fetchall()
        return [User(*a) for a in results] if results else []

    @staticmethod
    def get_one_by_id(id):

        statement = """
            SELECT *
            FROM user_account
            WHERE id = %s
            LIMIT 1;
        """
        with conn.cursor() as curs:
            curs.execute(statement, (id,))
            result = curs.fetchall()
        if not result:
            raise NotFoundErr
        return User(*result[0])

    @staticmethod
    def get_one_by_username(username):

        statement = """
            SELECT *
            FROM user_account
            WHERE username = %s
            LIMIT 1;
        """
        with conn.cursor() as curs:
            curs.execute(statement, (username,))
            result = curs.fetchall()
        if not result:
            raise NotFoundErr
        print(result)
        return User(*result[0])

    @staticmethod
    def create(username, password, role="user"):
        statement = "INSERT INTO user_account (username, password, role) VALUES (%s, %s) RETURNING *;"
        with conn.cursor() as curs:
            curs.execute(statement, (username, password, role))
            result = curs.fetchone()
            conn.commit()
            return User(*result)

    @staticmethod
    def validate_credentials(username, password):
        print("validating...")
        user = User.get_one_by_username(username)
        print(user.password, password)
        if checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
            return user
        else:
            raise Exception("Invalid credentials")


    def __init__(self, id, username, password, email, role):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def __repr__(self):
        return self.username

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }