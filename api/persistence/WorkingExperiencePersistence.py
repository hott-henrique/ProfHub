from api.persistence.connector import get_postgres_db


class WorkingExperiencePersistence(object):

    def create(self, working_experience: dict) -> int | None:
        uid = working_experience["uid"]
        job = working_experience["job"]
        company = working_experience["company"]
        starting_date = working_experience["starting_date"]
        ending_date = working_experience["ending_date"]
        description = working_experience["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    INSERT INTO ProfHub.WorkingExperience(uid, job, company, starting_date, ending_date, description)
                   	VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (uid, job, company, starting_date, ending_date, description)
            )

            data: dict = cursor.fetchone()

            return data['id'] if data else None

    def update(self, id: int, working_experience: dict):
        uid = working_experience["uid"]
        job = working_experience["job"]
        company = working_experience["company"]
        starting_date = working_experience["starting_date"]
        ending_date = working_experience["ending_date"]
        description = working_experience["description"]

        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    UPDATE ProfHub.WorkingExperience AS w
                    SET
                        uid = %s,
                        job = %s,
                        company = %s,
                        starting_date = %s,
                        ending_date = %s,
                        description = %s
                    WHERE a.id = %s;
                ''',
                (uid, job, company, starting_date, ending_date, description, id)
            )

            return cursor.rowcount != 0

    def delete(self, id: int):
        db = get_postgres_db()

        with db.cursor() as cursor:
            cursor.execute(
                '''
                    DELETE
                    FROM ProfHub.WorkingExperience AS w
                    WHERE w.id = %s;
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
                    FROM ProfHub.WorkingExperience AS w
                    WHERE a.uid = %s;
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
                    FROM ProfHub.WorkingExperience AS w
                    WHERE
                        w.job ILIKE %(query)s
                        OR
                        w.company ILIKE %(query)s
                        OR
                        w.description ILIKE %(query)s;
                ''',
                { "query": f"%{query}%" }
            )

            return cursor.fetchall()
