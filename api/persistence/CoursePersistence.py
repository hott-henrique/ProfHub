from api.persistence.connector import get_postgres_db


class CoursePersistence(object):

    def create(self, course: dict) -> int | None:
        uid = course["uid"]
        name = course["name"]
        date = course["date"]
        workload = course["workload"]
        description = course["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.Course(uid, name, date, workload, description)
                   	VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (uid, name, date, workload, description)
            )

            data: dict = cursor.fetchone()

            return data['id'] if data else None

    def update(self, id: int, course: dict):
        uid = course["uid"]
        name = course["name"]
        date = course["date"]
        workload = course["workload"]
        description = course["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.Course AS a
                    SET
                        uid = %s,
                        name = %s,
                        date = %s,
                        workload = %s,
                        description = %s
                    WHERE a.id = %s;
                ''',
                (uid, name, date, workload, description, id)
            )

            return cursor.rowcount != 0

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.Course AS c
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
                    FROM ProfHub.Course AS c
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
                    FROM ProfHub.Course AS c
                    WHERE
                        c.name ILIKE %(query)s
                        OR
                        c.description ILIKE %(query)s
                ''',
                { "query": f"%{query}%" }
            )

            return cursor.fetchall()
