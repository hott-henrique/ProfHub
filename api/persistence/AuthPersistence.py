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

    def update(self, id: int, new_hash: str) -> bool:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.Auth AS a
                    SET
                        password_hash = %s
                    WHERE a.uid = %s;
                ''',
                (new_hash, id)
            )

            return cursor.rowcount != 0

    def get_auth_info_by_uid(self, uid: int) -> dict:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.Auth AS a
                    WHERE a.uid = %s;
                ''',
                (uid, )
            )

            data: dict = cursor.fetchone()

            if not data:
                # TODO: RAISE ERROR.
                return None

            return data
