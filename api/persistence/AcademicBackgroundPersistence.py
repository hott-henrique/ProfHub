from api.persistence.connector import get_postgres_db


class AcademicBackgroundPersistence(object):

    def create(self, academic_background: dict) -> int | None:
        uid = academic_background["uid"]
        name = academic_background["name"]
        institution = academic_background["institution"]
        level = academic_background["level"]
        starting_date = academic_background["starting_date"]
        ending_date = academic_background["ending_date"]
        workload = academic_background["workload"]
        description = academic_background["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.AcademicBackground(uid, name, institution, level, starting_date, ending_date, workload, description)
                   	VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (uid, name, institution, level, starting_date, ending_date, workload, description)
            )

            data: dict = cursor.fetchone()

            return data['id'] if data else None

    def update(self, id: int, academic_background: dict):
        uid = academic_background["uid"]
        name = academic_background["name"]
        institution = academic_background["institution"]
        level = academic_background["level"]
        starting_date = academic_background["starting_date"]
        ending_date = academic_background["ending_date"]
        workload = academic_background["workload"]
        description = academic_background["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.AcademicBackground AS a
                    SET
                        uid = %s,
                        name = %s,
                        institution = %s,
                        level = %s,
                        starting_date = %s,
                        ending_date = %s,
                        workload = %s,
                        description = %s
                    WHERE a.id = %s;
                ''',
                (uid, name, institution, level, starting_date, ending_date, workload, description, id)
            )

            return cursor.rowcount != 0

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.AcademicBackground AS a
                    WHERE a.id = %s;
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
                    FROM ProfHub.AcademicBackground AS a
                    WHERE a.uid = %s;
                ''',
                (uid, )
            )

            return cursor.fetchall()

    def search(self, query: str, education_level: str | None = None) -> list[dict]:
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT *
                    FROM ProfHub.AcademicBackground AS a
                    WHERE
                        a.name ILIKE %(query)s
                        OR
                        a.institution ILIKE %(query)s;
                ''',
                { "query": f"%{query}%" }
            )

            data = cursor.fetchall()

            if education_level:
                data = list(filter(lambda obj: obj["level"] == education_level, data))

            return data
