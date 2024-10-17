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
