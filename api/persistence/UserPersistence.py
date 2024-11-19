import datetime as dt

from model.User import User

from api.persistence.connector import get_postgres_db


class UserPersistence(object):

    def create(self, user: dict) -> int:
        name = user["name"]
        email = user["email"]
        phone = user["phone"]
        github = user["github"]
        birthdate: dt.datetime = user["birthdate"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.User(name, email, phone, github, birthdate)
                    VALUES(%s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (name, email, phone, github, birthdate)
            )

            if cursor.rowcount != 1:
                # TODO: RAISE ERROR.
                return None

            data: dict = cursor.fetchone()

            if not data:
                # TODO: RAISE ERROR.
                return None

            return data['id']

    def update(self, id: int, user: dict) -> dict:
        name = user["name"]
        birthdate = user["starting_date"]
        email = user["email"]
        phone = user["phone"]
        github = user["github"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.User AS u
                    SET
                        name = %s,
                        birthdate = %s,
                        email = %s,
                        phone = %s,
                        github = %s
                    WHERE u.id = %s;
                ''',
                (name, birthdate, email, phone, github, id)
            )

            user["id"] = id

            return user

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.User AS u
                    WHERE u.id = %s;
                ''',
                (id, )
            )

            return cursor.rowcount != 0

    def get_by_email(self, email: str) -> dict:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.User AS u
                    WHERE u.email = %s;
                ''',
                (email, )
            )

            data: dict = cursor.fetchone()

            if not data:
                # TODO: RAISE ERROR.
                return None

            return data

    def get_by_id(self, id: int) -> dict:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.User AS u
                    WHERE u.id = %s;
                ''',
                (id, )
            )

            data: dict = cursor.fetchone()

            if not data:
                # TODO: RAISE ERROR.
                return None

            return data

    def search(self, query: str) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.User AS u
                    WHERE
                        u.name ILIKE %(query)s
                ''',
                { "query": f"%{query}%" }
            )

            return cursor.fetchall()
