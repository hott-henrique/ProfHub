from api.persistence.connector import get_postgres_db


class AuthPersistence(object):

    def create(self, auth: dict):
        id = auth["uid"]
        password_hash = auth["password_hash"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.Auth(uid, password_hash)
                    VALUES(%s, %s);
                ''',
                (id, password_hash)
            )

            if cursor.rowcount != 1:
                # TODO: RAISE ERROR.
                pass
