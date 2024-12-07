from api.persistence.connector import get_postgres_db


class CertificatePersistence(object):

    def create(self, certificate: dict) -> int | None:
        uid = certificate["uid"]
        name = certificate["name"]
        date = certificate["date"]
        validation_key = certificate["validation_key"]
        expire_date = certificate["expire_date"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.Certificate(uid, name, date, validation_key, expire_date)
                   	VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (uid, name, date, validation_key, expire_date)
            )

            data: dict = cursor.fetchone()

            return data['id'] if data else None

    def update(self, id: int, certificate: dict):
        uid = certificate["uid"]
        name = certificate["name"]
        date = certificate["date"]
        validation_key = certificate["validation_key"]
        expire_date = certificate["expire_date"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.Certificate AS c
                    SET
                        uid = %s,
                        name = %s,
                        date = %s,
                        validation_key = %s,
                        expire_date = %s
                    WHERE c.id = %s;
                ''',
                (uid, name, date, validation_key, expire_date, id)
            )

            return cursor.rowcount != 0

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.Certificate AS c
                    WHERE c.id = %s;
                ''',
                (id, )
            )

            return cursor.rowcount != 0

    def get_all_from_uid(self, uid: int) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.Certificate AS c
                    WHERE c.uid = %s;
                ''',
                (uid, )
            )

            return cursor.fetchall()

    def search(self, query: str) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.Certificate AS c
                    WHERE
                        c.name ILIKE %(query)s
                ''',
                { "query": f"%{query}%" }
            )

            return cursor.fetchall()
